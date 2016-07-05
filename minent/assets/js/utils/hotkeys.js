/**
 * utils/hotkeys.js
 * Keyboard hotkeys for the Maximum Entropy App
 *
 * Copyright (C) 2016 District Data Labs
 * For license information, see LICENSE.txt
 *
 * Author:  Benjamin Bengfort <bbengfort@districtdatalabs.com>
 * Created: Wed Jan 22 23:52:24 2014 -0500
 *
 * ID: hotkeys.js [] benjamin@bengfort.com $
 */


(function($) {
    $(document).ready(function() {

        $(document).keyup(function(e) {
            if (e.keyCode == 27) {
                e.preventDefault();
                window.location = "/admin/";
            }
        });

    });
})(jQuery);
