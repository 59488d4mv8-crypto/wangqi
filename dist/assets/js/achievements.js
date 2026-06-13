(function () {
  "use strict";

  var BADGES_URL = "assets/data/badges.json";
  var cachedBadges = null;

  function loadBadgesFile() {
    return fetch(BADGES_URL, { cache: "no-store" }).then(function (r) {
      if (!r.ok) throw new Error("加载徽章数据失败：" + r.status);
      return r.json();
    }).then(function (data) {
      cachedBadges = Array.isArray(data) ? data : [];
      return cachedBadges;
    });
  }

  function getCourseData() {
    return window.CourseData || null;
  }

  function firstCourseCompletedCheck() {
    var exams = window.LearnStore.getAllExamScores();
    var keys = Object.keys(exams);
    for (var i = 0; i < keys.length; i += 1) {
      var item = exams[keys[i]];
      if (item && item.passed) return true;
    }
    return false;
  }

  function courseCompletedCheck(id) {
    if (!id) return false;
    var record = window.LearnStore.getExamScore(id);
    return !!(record && record.passed);
  }

  function streakDaysCheck(n) {
    var days = window.LearnStore.getStreakDays();
    return days >= Number(n || 0);
  }

  function examFullScoreCheck() {
    var exams = window.LearnStore.getAllExamScores();
    var keys = Object.keys(exams);
    for (var i = 0; i < keys.length; i += 1) {
      var item = exams[keys[i]];
      if (item && item.score === 100) return true;
    }
    return false;
  }

  function totalPointsCheck(n) {
    return window.LearnStore.getTotalPoints() >= Number(n || 0);
  }

  function allChaptersReadCheck(id) {
    if (!id || !getCourseData()) return false;
    var store = window.LearnStore;
    var progress = store.getChapterProgress(id);
    var readSet = progress && progress.read ? progress.read : new Set();
    return new Promise(function (resolve) {
      getCourseData().loadById(id).then(function (course) {
        var chapters = course && Array.isArray(course.chapters) ? course.chapters : [];
        if (chapters.length === 0) return resolve(false);
        for (var i = 0; i < chapters.length; i += 1) {
          if (!readSet.has(String(chapters[i].id))) return resolve(false);
        }
        resolve(true);
      }).catch(function () {
        resolve(false);
      });
    });
  }

  function checkBadgeCondition(badge) {
    var condition = badge.condition || {};
    var type = condition.type || "";
    var value = condition.value;

    switch (type) {
      case "firstCourseCompleted":
        return Promise.resolve(firstCourseCompletedCheck());
      case "courseCompleted":
        return Promise.resolve(courseCompletedCheck(value));
      case "streakDays":
        return Promise.resolve(streakDaysCheck(value));
      case "examFullScore":
        return Promise.resolve(examFullScoreCheck());
      case "totalPoints":
        return Promise.resolve(totalPointsCheck(value));
      case "allChaptersRead":
        return allChaptersReadCheck(value);
      default:
        return Promise.resolve(false);
    }
  }

  function unlockBadge(badge) {
    var store = window.LearnStore;
    if (store.hasBadge(badge.id)) return false;
    store.recordBadge(badge.id);
    if (badge.points) store.addPoints(Number(badge.points) || 0, "badge:" + badge.id);
    try {
      window.dispatchEvent(new CustomEvent("learn:badgeUnlocked", {
        detail: { badgeId: badge.id, title: badge.title, points: Number(badge.points) || 0 }
      }));
    } catch (e) {
      // ignore
    }
    return true;
  }

  var Achievements = {
    loadAll: function () {
      if (cachedBadges) return Promise.resolve(cachedBadges.slice());
      return loadBadgesFile();
    },
    getCached: function () {
      return cachedBadges ? cachedBadges.slice() : [];
    },
    checkAll: function (course) {
      var self = this;
      return this.loadAll().then(function (badges) {
        var checks = badges.map(function (badge) {
          if (window.LearnStore.hasBadge(badge.id)) return Promise.resolve({ badge: badge, met: false, already: true });
          return checkBadgeCondition(badge).then(function (met) {
            return { badge: badge, met: !!met, already: false };
          });
        });
        return Promise.all(checks).then(function (results) {
          var unlocked = [];
          for (var i = 0; i < results.length; i += 1) {
            var r = results[i];
            if (!r.already && r.met) {
              if (unlockBadge(r.badge)) unlocked.push(r.badge);
            }
          }
          return {
            course: course,
            badges: badges,
            unlocked: unlocked,
            totalPoints: window.LearnStore.getTotalPoints(),
            earnedCount: window.LearnStore.getBadges().length
          };
        });
      });
    }
  };

  window.Achievements = Achievements;
})();
