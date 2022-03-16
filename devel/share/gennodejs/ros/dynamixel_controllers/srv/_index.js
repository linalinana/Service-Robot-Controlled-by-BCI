
"use strict";

let SetComplianceSlope = require('./SetComplianceSlope.js')
let SetCompliancePunch = require('./SetCompliancePunch.js')
let RestartController = require('./RestartController.js')
let SetSpeed = require('./SetSpeed.js')
let SetComplianceMargin = require('./SetComplianceMargin.js')
let StartController = require('./StartController.js')
let SetTorqueLimit = require('./SetTorqueLimit.js')
let StopController = require('./StopController.js')
let TorqueEnable = require('./TorqueEnable.js')

module.exports = {
  SetComplianceSlope: SetComplianceSlope,
  SetCompliancePunch: SetCompliancePunch,
  RestartController: RestartController,
  SetSpeed: SetSpeed,
  SetComplianceMargin: SetComplianceMargin,
  StartController: StartController,
  SetTorqueLimit: SetTorqueLimit,
  StopController: StopController,
  TorqueEnable: TorqueEnable,
};
