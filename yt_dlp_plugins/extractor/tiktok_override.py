from yt_dlp.utils import ExtractorError, traverse_obj
from yt_dlp.extractor.tiktok import TikTokIE



class Override_TikTokIE(TikTokIE, plugin_name='fix'):
    def _get_sigi_state(self, webpage, display_id):
        return self._search_json(
            r'<script[^>]+\bid="(?:SIGI_STATE|sigi-persisted-data|__UNIVERSAL_DATA_FOR_REHYDRATION__)"[^>]*>', webpage,
            'sigi state', display_id, end_pattern=r'</script>')
    def _real_extract(self, url):
        video_id, user_id = self._match_valid_url(url).group('id', 'user_id')
        try:
            return self._extract_aweme_app(video_id)
        except ExtractorError as e:
            self.report_warning(f'{e}; trying with webpage')

        url = self._create_url(user_id, video_id)
        webpage = self._download_webpage(url, video_id, headers={'User-Agent': 'Mozilla/5.0'})
        next_data = self._search_nextjs_data(webpage, video_id, default='{}')
        if next_data:
            status = traverse_obj(next_data, ('props', 'pageProps', 'statusCode'), expected_type=int) or 0
            video_data = traverse_obj(next_data, ('props', 'pageProps', 'itemInfo', 'itemStruct'), expected_type=dict)
        else:
            sigi_data = self._get_sigi_state(webpage, video_id)
            status = traverse_obj(sigi_data, ('VideoPage', 'statusCode'), expected_type=int) or 0
            video_data = traverse_obj(sigi_data, ('ItemModule', video_id), (...,...,'itemInfo', 'itemStruct'), expected_type=dict, get_all=False)

        if status == 0:
            return self._parse_aweme_video_web(video_data, url, video_id)
        elif status == 10216:
            raise ExtractorError('This video is private', expected=True)
        raise ExtractorError('Video not available', video_id=video_id)


__all__ = []
