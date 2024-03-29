# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import flask
import RPi.GPIO as GPIO

class GaioPlugin(octoprint.plugin.StartupPlugin,
				octoprint.plugin.SettingsPlugin,
				octoprint.plugin.AssetPlugin,
				octoprint.plugin.TemplatePlugin,
				octoprint.plugin.SimpleApiPlugin):
	light_state = "On"

	def on_after_startup(self):
		GPIO.setmode(GPIO.BCM) # TODO: Rendere selezionabile da config
		GPIO.setup(int(self._settings.get(["pin_light"])), GPIO.OUT)
		GPIO.output(int(self._settings.get(["pin_light"])), GPIO.LOW)
		self._logger.info(octoprint.util.platform.get_os())
		self.update_icon()
	
	def on_settings_save(self, data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
		GPIO.setup(int(self._settings.get(["pin_light"])), GPIO.OUT)
		GPIO.output(int(self._settings.get(["pin_light"])), GPIO.LOW)
		self.update_icon()

	def get_api_commands(self):
		return dict(
			light_toggle=[]
		)

	def on_api_command(self, command, data):
		if command == "light_toggle":
			self.update_icon()
			self._logger.info(self.light_state)
			return flask.jsonify(status="ok", light_state=self.light_state)
			
	def on_api_get(self, request):
		return flask.jsonify(status="ok", pin_light=self._settings.get(["pin_light"]))

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			pin_light="0"
		)

	##~~ AssetPlugin mixin

	def get_assets(self):
		return dict(
			js=["js/gaio.js"],
			css=["css/gaio.css"],
			less=["less/gaio.less"]
		)

	def get_template_configs(self):
		return [
        	dict(type="settings", custom_bindings=False)
    	]

	def get_template_vars(self):
		return dict(
			pin_light=self._settings.get(["pin_light"]),
		)

	# Cose nostre
	def update_icon(self):
		if(self.light_state=="On"):
			GPIO.output(int(self._settings.get(["pin_light"])), GPIO.HIGH)
			self.light_state = "Off"
		else:
			GPIO.output(int(self._settings.get(["pin_light"])), GPIO.LOW)
			self.light_state = "On"

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
		# for details.
		return dict(
			gaio=dict(
				displayName="Gaio Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="nonzod",
				repo="OctoPrint-Gaio",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/nonzod/OctoPrint-Gaio/archive/{target_version}.zip"
			)
		)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Gaio Plugin"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
__plugin_pythoncompat__ = ">=3,<4" # only python 3
#__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = GaioPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}