{
        $(document).ready(function() {
            $('.bookmark-btn').on('click', function() {
                var btn = $(this);
                var songId = btn.data('song-id');
                var csrfToken = $('meta[name="csrf-token"]').attr('content');
        
                $.ajax({
                    url: '/bookmark/song/',  // 북마크 처리를 위한 URL
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': csrfToken,
                        'song_id': songId
                    },
                    success: function(data) {
                        if (data.status == 'added') {
                            btn.html('<i class="bi bi-bookmark-fill"></i>'); // 북마크 해제 아이콘
                        } else {
                            btn.html('<i class="bi bi-bookmark"></i>'); // 북마크 설정 아이콘
                        }
                    },
                    error: function(xhr, status, error) {
                        console.error("AJAX 요청 실패:", status, error);
                    }
                });
            });
        });
}