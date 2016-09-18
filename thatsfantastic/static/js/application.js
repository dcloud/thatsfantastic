"use strict";

Zepto(function($) {
  $('select[name="event"]').on('change', function (event) {
    var event_value = $(event.target).val();
    if (event_value != null) document.location = event.target.value;
  });

    $('.top-bar').each(function(index, el) {
        var bar = $(el);
        var togglers = bar.find('.toggle-topbar > a');
        var barSections = bar.find('.top-bar-section');
        togglers.on('click', function(event) {
            barSections.toggle();
        });
        barSections.hide();
    });

    $('.tab-bar').each(function(index, element) {
        var bar = $(element);
        var tabButtons = bar.find('li > a');
        var tabs = $('.tab-sections > section');
        tabs.hide();

        tabButtons.each(function(index, el) {
            var href = $(el).attr('href');
            var enabled = false;
            if (href.charAt(0) == "#") {
                $(el).data('href', href);
                enabled = true;
            }
            $(el).data('tab-enabled', enabled);
        }).on('click', function(event) {
            event.preventDefault();
            var tabButton = $(this);
            tabButton.addClass('active');
            tabButtons.not(tabButton).removeClass('active');
            var dhref = tabButton.data('href');
            if (dhref.charAt(0) == "#") {
                tabs.not(dhref).hide();
                $(dhref).show();
            }
        });

        if (!document.location.hash) {
            tabs.first().show();
            tabButtons.first().addClass('active');
        } else {
            tabButtons.filter("[href=" + document.location.hash + "]").click();
        }
    });
});
