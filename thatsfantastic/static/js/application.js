"use strict";

jQuery(document).ready(function($) {
    $('.top-bar').each(function(index, el) {
        console.log('Hi')
        var bar = $(el);
        var togglers = bar.find('.toggle-topbar > a');
        var barSections = bar.find('.top-bar-section');
        togglers.on('click', function(event) {
            barSections.slideToggle('fast');
        });
        barSections.hide();
    });
});