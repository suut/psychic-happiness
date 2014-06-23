## account.py
# Account system support.
from pydle.features import rfc1459

class AccountSupport(rfc1459.RFC1459Support):

    ## Internal.

    def _create_user(self, nickname):
        super()._create_user(nickname)
        if nickname in self.users:
            self.users[nickname].update({
                'account': None,
                'identified': False
            })

    def _rename_user(self, user, new):
        super()._rename_user(user, new)
        # Unset account info.
        self._sync_user(new, { 'account': None, 'identified': False })


    ## IRC API.

    def whois(self, nickname):
        future = super().whois(nickname)

        # Add own info.
        if nickname in self._whois_info:
            self._whois_info[nickname].setdefault('account', None)
            self._whois_info[nickname].setdefault('identified', False)

        return future


    ## Message handlers.

    def on_raw_307(self, message):
        """ WHOIS: User has identified for this nickname. (Anope) """
        target, nickname = message.params[:2]
        info = {
            'identified': True
        }

        if nickname in self.users:
            self._sync_user(nickname, info)
        if nickname in self._pending['whois']:
            self._whois_info[nickname].update(info)

    def on_raw_330(self, message):
        """ WHOIS account name (Atheme). """
        target, nickname, account = message.params[:3]
        info = {
            'account': account,
            'identified': True
        }

        if nickname in self.users:
            self._sync_user(nickname, info)
        if nickname in self._pending['whois']:
            self._whois_info[nickname].update(info)
