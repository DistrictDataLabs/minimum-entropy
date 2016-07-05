/**
 * utils/hotkeys.js
 * Keyboard hotkeys for the Ronin App
 *
 * Copyright (C) 2014 University of Maryland
 * For license information, see LICENSE.txt
 *
 * Author:  Benjamin Bengfort <bengfort@cs.umd.edu>
 * Created: Wed Jan 22 23:52:24 2014 -0500
 *
 * ID: hotkeys.js [] bengfort@cs.umd.edu $
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
