import logging


class LogHandler(logging.Handler):

    def __init__(self, plugin_name, collectd):
        self.plugin_name = plugin_name
        self.collectd = collectd

        logging.Handler.__init__(self)

    def emit(self, record):
        try:
            if record.msg is not None:
                if record.levelname == 'ERROR':
                    self.collectd.error('%s: %s' % (self.plugin_name, record.msg))
                elif record.levelname == 'WARNING':
                    self.collectd.warning('%s: %s' % (self.plugin_name, record.msg))
                elif record.levelname == 'INFO':
                    self.collectd.info('%s: %s' % (self.plugin_name, record.msg))
                elif record.levelname == 'DEBUG':
                    self.collectd.debug('%s: %s' % (self.plugin_name, record.msg))
        except Exception as exception:
            self.collectd.warning(('{0}: Failed to write log statement due to: {1}').format(self.plugin_name, exception))
