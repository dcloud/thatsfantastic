var gulp = require('gulp'),
    streamqueue = require('streamqueue'),
    concat = require('gulp-concat'),
    minifyCSS = require('gulp-minify-css'),
    sass = require('gulp-ruby-sass'),
    rename = require('gulp-rename'),
    browserSync = require('browser-sync'),
    reload = browserSync.reload;

var staticDir = 'thatsfantastic/static/',
    cssDir = staticDir + 'css/',
    sassDir = staticDir + 'sass/';

gulp.task('sass', function() {
    return sass(sassDir)
    .on('error', sass.logError)
    .pipe(concat('main.css'))
    .pipe(gulp.dest(cssDir))
    .pipe(minifyCSS())
    .pipe(rename({ extname: '.min.css' }))
    .pipe(gulp.dest(cssDir))
});

gulp.task('build', ['sass'])

// watch files for changes and reload
gulp.task('watch', function() {
  gulp.watch(sassDir + '*.scss', ['sass', reload]);
});

gulp.task('default', ['build'])