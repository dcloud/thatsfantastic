var gulp = require('gulp'),
    streamqueue = require('streamqueue'),
    concat = require('gulp-concat'),
    minifyCSS = require('gulp-minify-css'),
    sass = require('gulp-ruby-sass'),
    rename = require('gulp-rename'),
    babel = require("gulp-babel"),
    browserSync = require('browser-sync'),
    reload = browserSync.reload;

var staticDir = 'thatsfantastic/static/',
    cssDir = staticDir + 'css/',
    sassDir = staticDir + 'sass/',
    es6Dir = staticDir + 'js/src/',
    jsDir = staticDir + 'js/';

gulp.task('sass', function() {
    return sass(staticDir + 'sass/application.scss')
    .pipe(concat('main.css'))
    .pipe(gulp.dest(cssDir))
    .pipe(minifyCSS())
    .pipe(rename({ extname: '.min.css' }))
    .pipe(gulp.dest(cssDir))
});

gulp.task('js', function() {
    return gulp.src(es6Dir + '*.js')
    .pipe(concat('site.js'))
    .pipe(babel())
    .pipe(gulp.dest(jsDir));
});


gulp.task('build', ['sass', 'js'])

// watch files for changes and reload
gulp.task('watch', function() {
  gulp.watch([sassDir + '*.scss', es6Dir + '*.js'], ['sass', 'js', reload]);
});

gulp.task('default', ['build'])