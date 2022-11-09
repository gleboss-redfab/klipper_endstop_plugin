import logging
import pins

class Endstop:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.name = config.get_name().split()[-1]
        self.last_state = False
        self.gcode = self.printer.lookup_object('gcode')
        logging.error("CUSTOM ENDSTOP %s INITIALIZATION", self.name)

        # get (spizdil) from probe.py module 
        ppins = self.printer.lookup_object('pins')
        pin = config.get('pin')
        pin_params = ppins.lookup_pin(pin, can_invert=True, can_pullup=True)
        mcu = pin_params['chip']
        self.mcu_endstop = mcu.setup_pin('endstop', pin_params)

        # Register QUERY_ENDSTOP command with ENDSTOP=<name> param
        self.gcode.register_mux_command('QUERY_ENDSTOP', "ENDSTOP", self.name, self.cmd_QUERY_ENDSTOP)
    
    # read enstop and write to memory
    def _update_endstope_state(self):
        # algorithm get (spizdil) from probe.py module 
        # it is not work without print_time value
        toolhead = self.printer.lookup_object('toolhead')
        print_time = toolhead.get_last_move_time()
        res = self.mcu_endstop.query_endstop(print_time)
        
        self.last_state = res

    # run custom QUERY_ENDSTOP macros
    def cmd_QUERY_ENDSTOP(self, gcmd):
        self._update_endstope_state()
        gcmd.respond_info("%s : %s" % (self.name ,["open", "TRIGGERED"][self.last_state],))


    # save as internal parameter for access from gcode's macroses 
    def get_status(self, eventtime):
        return {'state': self.last_state}


def load_config_prefix(config):
    return Endstop(config)