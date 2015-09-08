"use strict";

jQuery(document).ready(function($) {
    $('.top-bar').each(function(index, el) {
        var bar = $(el);
        var togglers = bar.find('.toggle-topbar > a');
        var barSections = bar.find('.top-bar-section');
        togglers.on('click', function(event) {
            barSections.slideToggle('fast');
        });
        barSections.hide();
    });

    $('.tab-bar').each(function(index, element) {
        var bar = $(element);
        var tabButtons = bar.find('li > a');
        var tabs = $('.tab-sections > section');
        tabs.hide();

        tabButtons.on('click', function(event) {
            var tabButton = $(this);
            tabButton.addClass('active');
            tabButtons.not(tabButton).removeClass('active');
            var href = tabButton.attr('href');
            if (href.charAt(0) == "#") {
                tabs.not(href).hide();
                $(href).show();
            }
        });

        if (!document.location.hash) {
            tabs.first().show();
            tabButtons.first().addClass('active');
            document.location.hash = tabs.first().attr('id');
        } else {
            tabButtons.filter("[href=" + document.location.hash + "]").click();
        }
    });
});