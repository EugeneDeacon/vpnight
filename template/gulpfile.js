const gulp = require("gulp");
const inlineSource = require("gulp-inline-source");
const htmlmin = require("gulp-htmlmin");

function buildHtml() {
  return gulp
    .src("templates/main.html")
    .pipe(inlineSource({ compress: false }))
    .pipe(htmlmin({ collapseWhitespace: true, removeComments: true }))
    .pipe(gulp.dest("dist"));
}

exports.default = buildHtml;
