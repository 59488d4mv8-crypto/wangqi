(function () {
  "use strict";

  var PREFIX = "learn_";

  function fullKey(key) {
    return PREFIX + key;
  }

  function safeParse(raw) {
    if (raw == null) return null;
    try {
      return JSON.parse(raw);
    } catch (e) {
      return raw;
    }
  }

  function readSet(key) {
    var data = safeParse(localStorage.getItem(fullKey(key)));
    if (Array.isArray(data)) {
      var set = new Set();
      for (var i = 0; i < data.length; i += 1) set.add(data[i]);
      return set;
    }
    return new Set();
  }

  function writeSet(key, set) {
    var arr = [];
    set.forEach(function (v) {
      arr.push(v);
    });
    localStorage.setItem(fullKey(key), JSON.stringify(arr));
  }

  var LearnStore = {
    read: function (key) {
      return safeParse(localStorage.getItem(fullKey(key)));
    },
    write: function (key, value) {
      if (value instanceof Set) {
        var arr = [];
        value.forEach(function (v) {
          arr.push(v);
        });
        localStorage.setItem(fullKey(key), JSON.stringify(arr));
      } else if (typeof value === "object") {
        localStorage.setItem(fullKey(key), JSON.stringify(value));
      } else {
        localStorage.setItem(fullKey(key), JSON.stringify(value));
      }
    },
    remove: function (key) {
      localStorage.removeItem(fullKey(key));
    },

    markChapterRead: function (courseId, chapterId) {
      var key = "progress:" + courseId + ":chaptersRead";
      var set = readSet(key);
      set.add(String(chapterId));
      writeSet(key, set);
      this.recordRecentCourse(courseId);
      window.dispatchEvent(new CustomEvent("learn:chapterRead", { detail: { courseId: courseId, chapterId: chapterId } }));
    },
    getChapterProgress: function (courseId) {
      var key = "progress:" + courseId + ":chaptersRead";
      return { read: readSet(key) };
    },

    saveChapterScore: function (courseId, chapterId, score) {
      var key = "progress:" + courseId + ":scores";
      var data = safeParse(localStorage.getItem(fullKey(key))) || {};
      data[String(chapterId)] = Number(score) || 0;
      localStorage.setItem(fullKey(key), JSON.stringify(data));
    },
    getChapterScore: function (courseId, chapterId) {
      var key = "progress:" + courseId + ":scores";
      var data = safeParse(localStorage.getItem(fullKey(key))) || {};
      var score = data[String(chapterId)];
      if (typeof score === "number") return score;
      return 0;
    },
    getAllChapterScores: function (courseId) {
      var key = "progress:" + courseId + ":scores";
      return safeParse(localStorage.getItem(fullKey(key))) || {};
    },

    saveExamScore: function (courseId, score, passed, dateString) {
      var key = "exam:" + courseId;
      var data = {
        score: Number(score) || 0,
        passed: !!passed,
        date: dateString || new Date().toISOString().slice(0, 10)
      };
      localStorage.setItem(fullKey(key), JSON.stringify(data));
      this.recordRecentCourse(courseId);
    },
    getExamScore: function (courseId) {
      var key = "exam:" + courseId;
      return safeParse(localStorage.getItem(fullKey(key))) || null;
    },
    getAllExamScores: function () {
      var result = {};
      for (var i = 0; i < localStorage.length; i += 1) {
        var k = localStorage.key(i);
        if (k && k.indexOf(PREFIX + "exam:") === 0) {
          var courseId = k.slice((PREFIX + "exam:").length);
          result[courseId] = safeParse(localStorage.getItem(k));
        }
      }
      return result;
    },

    touchVisitDay: function (dateString) {
      var key = "visits";
      var set = readSet(key);
      set.add(String(dateString));
      writeSet(key, set);
      return this.getStreakDays();
    },
    getVisitDays: function () {
      var set = readSet("visits");
      var arr = [];
      set.forEach(function (d) {
        arr.push(d);
      });
      arr.sort();
      return arr;
    },
    getRecentVisitDays: function (days) {
      var n = days || 7;
      var visits = this.getVisitDays();
      var visitSet = {};
      for (var i = 0; i < visits.length; i += 1) visitSet[visits[i]] = true;
      var result = [];
      var today = new Date();
      for (var j = n - 1; j >= 0; j -= 1) {
        var d = new Date(today.getFullYear(), today.getMonth(), today.getDate() - j);
        var iso = d.toISOString().slice(0, 10);
        result.push({ date: iso, visited: !!visitSet[iso], label: (d.getMonth() + 1) + "/" + d.getDate() });
      }
      return result;
    },
    getStreakDays: function () {
      var visits = this.getVisitDays();
      if (visits.length === 0) return 0;
      var visitSet = {};
      for (var i = 0; i < visits.length; i += 1) visitSet[visits[i]] = true;
      var streak = 0;
      var today = new Date();
      var cursor = new Date(today.getFullYear(), today.getMonth(), today.getDate());
      while (visitSet[cursor.toISOString().slice(0, 10)]) {
        streak += 1;
        cursor.setDate(cursor.getDate() - 1);
      }
      if (streak === 0) {
        var yest = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 1);
        if (visitSet[yest.toISOString().slice(0, 10)]) {
          var s = 1;
          var c = new Date(yest);
          c.setDate(c.getDate() - 1);
          while (visitSet[c.toISOString().slice(0, 10)]) {
            s += 1;
            c.setDate(c.getDate() - 1);
          }
          streak = s;
        }
      }
      return streak;
    },

    recordBadge: function (badgeId) {
      var set = readSet("badges");
      set.add(String(badgeId));
      writeSet("badges", set);
    },
    hasBadge: function (badgeId) {
      var set = readSet("badges");
      return set.has(String(badgeId));
    },
    getBadges: function () {
      var set = readSet("badges");
      var arr = [];
      set.forEach(function (b) { arr.push(b); });
      return arr;
    },

    addPoints: function (delta, reason) {
      var key = "totalPoints";
      var current = Number(localStorage.getItem(fullKey(key))) || 0;
      current = current + Number(delta || 0);
      if (current < 0) current = 0;
      localStorage.setItem(fullKey(key), String(current));
      var historyKey = "pointsHistory";
      var history = safeParse(localStorage.getItem(fullKey(historyKey))) || [];
      history.push({
        delta: Number(delta || 0),
        reason: reason || "",
        total: current,
        date: new Date().toISOString().slice(0, 10)
      });
      if (history.length > 200) history = history.slice(history.length - 200);
      localStorage.setItem(fullKey(historyKey), JSON.stringify(history));
      return current;
    },
    getTotalPoints: function () {
      return Number(localStorage.getItem(fullKey("totalPoints"))) || 0;
    },

    recordRecentCourse: function (courseId) {
      var key = "recentCourses";
      var recent = safeParse(localStorage.getItem(fullKey(key))) || [];
      var filtered = [];
      for (var i = 0; i < recent.length; i += 1) {
        if (recent[i] !== courseId) filtered.push(recent[i]);
      }
      filtered.unshift(courseId);
      if (filtered.length > 10) filtered = filtered.slice(0, 10);
      localStorage.setItem(fullKey(key), JSON.stringify(filtered));
    },
    getRecentCourses: function () {
      var key = "recentCourses";
      return safeParse(localStorage.getItem(fullKey(key))) || [];
    },

    exportData: function () {
      var out = {};
      for (var i = 0; i < localStorage.length; i += 1) {
        var k = localStorage.key(i);
        if (k && k.indexOf(PREFIX) === 0) {
          out[k] = localStorage.getItem(k);
        }
      }
      return out;
    },
    resetAll: function () {
      var toRemove = [];
      for (var i = 0; i < localStorage.length; i += 1) {
        var k = localStorage.key(i);
        if (k && k.indexOf(PREFIX) === 0) {
          toRemove.push(k);
        }
      }
      for (var j = 0; j < toRemove.length; j += 1) {
        localStorage.removeItem(toRemove[j]);
      }
    }
  };

  window.LearnStore = LearnStore;
})();
