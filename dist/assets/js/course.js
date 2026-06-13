(function () {
  "use strict";

  function normalize(str) {
    if (str == null) return "";
    return String(str).trim().toLowerCase();
  }

  function compareSets(a, b) {
    if (a == null || b == null) return false;
    var sa = new Set();
    var arr = Array.isArray(a) ? a : [a];
    for (var i = 0; i < arr.length; i += 1) sa.add(normalize(arr[i]));

    var sb = new Set();
    var brr = Array.isArray(b) ? b : [b];
    for (var j = 0; j < brr.length; j += 1) sb.add(normalize(brr[j]));

    if (sa.size !== sb.size) return false;
    var iter = sa.values();
    var v = iter.next();
    while (!v.done) {
      if (!sb.has(v.value)) return false;
      v = iter.next();
    }
    return true;
  }

  function collectAnswers(answer) {
    if (Array.isArray(answer)) return answer.slice();
    if (answer == null || answer === "") return [];
    return [answer];
  }

  function gradeQuizAnswer(quizItem, userAnswer) {
    var type = quizItem && quizItem.type;
    var correct = false;
    var score = 0;

    if (type === "single") {
      var right = normalize(quizItem.answer);
      var ua = normalize(userAnswer);
      correct = ua === right;
      score = correct ? 100 : 0;
    } else if (type === "multiple") {
      var expected = collectAnswers(quizItem.answer);
      var given = Array.isArray(userAnswer) ? userAnswer.slice() : [userAnswer];
      correct = compareSets(expected, given);
      score = correct ? 100 : 0;
    } else if (type === "text") {
      var expectedList = collectAnswers(quizItem.answer);
      var givenNorm = normalize(userAnswer);
      if (givenNorm) {
        for (var i = 0; i < expectedList.length; i += 1) {
          if (givenNorm.indexOf(normalize(expectedList[i])) !== -1) {
            correct = true;
            break;
          }
          if (normalize(expectedList[i]).indexOf(givenNorm) !== -1 && givenNorm.length >= 2) {
            correct = true;
            break;
          }
        }
      }
      score = correct ? 100 : 0;
    } else if (type === "code") {
      var expectedLines = Array.isArray(quizItem.answerLines) ? quizItem.answerLines : [];
      var userLines = [];
      if (Array.isArray(userAnswer)) {
        userLines = userAnswer.slice();
      } else if (typeof userAnswer === "string") {
        userLines = userAnswer.split(/\r?\n/);
      }
      var match = true;
      var len = Math.min(expectedLines.length, userLines.length);
      if (len === 0) match = false;
      for (var k = 0; k < len; k += 1) {
        if (normalize(expectedLines[k]) !== normalize(userLines[k])) {
          match = false;
          break;
        }
      }
      if (expectedLines.length !== userLines.length) match = false;
      correct = match;
      score = correct ? 100 : 0;
    } else {
      correct = false;
      score = 0;
    }

    return { correct: correct, score: score };
  }

  function loadIndex() {
    return fetch("assets/data/courses/index.json", { cache: "no-store" }).then(function (r) {
      if (!r.ok) throw new Error("加载课程目录失败：" + r.status);
      return r.json();
    });
  }

  function loadById(id) {
    if (!id) return Promise.reject(new Error("缺少课程 id"));
    return fetch("assets/data/courses/" + encodeURIComponent(id) + ".json", { cache: "no-store" }).then(function (r) {
      if (!r.ok) throw new Error("加载课程失败：" + r.status);
      return r.json();
    });
  }

  window.CourseData = {
    loadIndex: loadIndex,
    loadById: loadById,
    gradeQuizAnswer: gradeQuizAnswer,
    normalize: normalize,
    compareSets: compareSets
  };
})();
