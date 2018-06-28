/* TODO copy right header? */

Blockly.defineBlocksWithJsonArray([{
  "type": "gpio",
  "message0": " write to pin %1 with value %2 ",
  "args0": [
  {
    "type": "field_number",
    "name": "PIN",
    "min": 0,
    "max": 31,
    "value": 2
  },
  {
    "type": "field_number",
    "name": "VALUE",
    "min": 0,
    "max": 1,
    "value": 1
  }
  ],
  "previousStatement": null,
  "nextStatement": null,
  "colour": "%{BKY_LOOPS_HUE}"
}]);

/**
 * Generator for gpio block creates call to new method
 * <code>gpio()</code>.
 */
Blockly.JavaScript['gpio'] = function(block) {
  var pin = Number(block.getFieldValue('PIN'));
  var value = Number(block.getFieldValue('VALUE'));
  var code = 'gpioWritePwm(' + pin + ',' + value + ');\n';
  return code;
};

function httpPostAsync(theUrl, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("POST", theUrl, true); // true for asynchronous 
    xmlHttp.send(null);
}

/**
 * Register the interpreter asynchronous function
 * <code>gpio()</code>.
 */
function initInterpreterGpioWritePwm(interpreter, scope) {
  // Ensure function name does not conflict with variable names.
  Blockly.JavaScript.addReservedWords('gpioWritePwm');

  var wrapper = interpreter.createAsyncFunction(
    function(pin, value, callback) {
      httpPostAsync("/pwm?pin="+pin+"&value="+value,function(x){
      });
      // Delay the call to the callback.
      setTimeout(callback, 10);
    });
  interpreter.setProperty(scope, 'gpioWritePwm', wrapper);
}
