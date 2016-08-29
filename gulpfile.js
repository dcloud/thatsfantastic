'use strict';

var gulp = require('gulp'),
    concat = require('gulp-concat'),
    cleanCSS = require('gulp-clean-css'),
    sass = require('gulp-sass'),
    sourcemaps  = require('gulp-sourcemaps'),
    rename = require('gulp-rename'),
    browserSync = require('browser-sync').create();

var staticDir = 'thatsfantastic/static/',
    cssDir = staticDir + 'css/',
    sassDir = staticDir + 'sass/',
    sassGlob = '/**/*.scss';

gulp.task('sass', function() {
  return gulp.src(sassDir + sassGlob)
             .pipe(sourcemaps.init())
             .pipe(sass().on('error', sass.logError))
             .pipe(cleanCSS({processImportFrom: ['local']}))
             .pipe(concat('main.min.css'))
             .pipe(sourcemaps.write('./maps'))
             .pipe(gulp.dest(cssDir))
             .pipe(browserSync.stream());
});

gulp.task('build', ['sass'])

// watch files for changes and reload
gulp.task('serve', ['sass'], function() {
  gulp.watch(sassDir + sassGlob, ['sass']);
  browserSync.init({
    proxy: "localhost:8000",
    serveStatic: [staticDir],
    files: [cssDir + '*.css'],
    open: false
  });

});

gulp.task('default', ['build'])
