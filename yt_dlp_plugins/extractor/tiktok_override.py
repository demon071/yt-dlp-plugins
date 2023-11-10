from yt_dlp.extractor.tiktok import TikTokBaseIE

# ⚠ Other plugins cannot be overridden using this method
# ⚠ The extractor internals may change without warning, breaking the plugin



class _TikTokOverrideTikTokIE(TikTokBaseIE, plugin_name='tiktok1'):
    def _get_sigi_state(self, webpage, display_id):
        return self._search_json(
            r'<script[^>]+\bid="(?:SIGI_STATE|sigi-persisted-data|__UNIVERSAL_DATA_FOR_REHYDRATION__)"[^>]*>', webpage,
            'sigi state', display_id, end_pattern=r'</script>')
    def _real_extract(self, url):
        self.to_screen('Passing through SampleOverridePluginIE')
        return super()._real_extract(url)
