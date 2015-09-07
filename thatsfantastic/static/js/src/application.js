"use strict";

(function() {
    function hideElements (elementsList) {
        for (let element of elementsList) {
            element.style.display = 'none';
        }
    }

    document.addEventListener('readystatechange', function(event) {
        if (document.readyState === 'interactive') {
            let barSectionElements = document.getElementsByClassName('top-bar-section');
            hideElements(barSectionElements);
        };
    });
})()