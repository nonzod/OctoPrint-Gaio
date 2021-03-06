/*
 * View model for OctoPrint-Gaio
 *
 * Author: Nicola Tomassoni
 * License: AGPLv3
 */
$(function() {
    function GaioViewModel(parameters) {
        var self = this;
        self.settings = parameters[0];
        self.pin_light = ko.observable("");
        self.lightStatus = ko.observable("");

        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];

        self.onBeforeBinding = function() {
            self.pin_light(self.settings.settings.plugins.gaio.pin_light());
            self.lightStatus('<i class="far fa-lightbulb"></i>');
        }

        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "gaio") {
                return;
            }
        }

        self.toggleLight = function(actual) {
            OctoPrint.simpleApiCommand("gaio", "light_toggle")
                .done(function(response) {
                    if (response.light_state == "On") {
                        self.lightStatus('<i class="fas fa-lightbulb" style="color: yellow"></i>');
                    } else {
                        self.lightStatus('<i class="far fa-lightbulb"></i>');
                    }
                    console.log(self.lightStatus);
                });

            return { "light_state" : self.lightStatus };
        }
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: GaioViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ "settingsViewModel" ],
        // Elements to bind to, e.g. #settings_plugin_gaio, #tab_plugin_gaio, ...
        elements: [ "#navbar_plugin_gaio" ]
    });
});
