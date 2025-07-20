const scriptName = "YouTube 요약 봇";

/**
 * YouTube URL을 감지하여 자막을 추출하고 AI로 요약하는 봇
 */
function response(room, msg, sender, isGroupChat, replier) {
    // YouTube URL 패턴 확인
    if (msg.includes("youtu.be/") || msg.includes("youtube.com/watch")) {
        try {
            // 즉시 처리 시작 메시지 보내기
            replier.reply("🔄 YouTube 영상 요약 중입니다... 잠시만 기다려주세요!");
            
            // HTTP 요청 데이터 준비
            var data = JSON.stringify({
                "msg": msg,
                "sender": sender,
                "room": room
            });
            
            // HTTP 연결 설정 (타임아웃 시간 대폭 증가)
            var url = new java.net.URL("http://192.168.0.15:8080/youtube");
            var connection = url.openConnection();
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json");
            connection.setDoOutput(true);
            
            // 타임아웃 시간 증가 (기본 5초 → 120초)
            connection.setConnectTimeout(30000);  // 연결 타임아웃: 30초
            connection.setReadTimeout(120000);    // 읽기 타임아웃: 120초
            
            // 요청 데이터 전송
            var outputStream = connection.getOutputStream();
            var writer = new java.io.OutputStreamWriter(outputStream, "UTF-8");
            writer.write(data);
            writer.flush();
            writer.close();
            
            // 응답 받기
            var responseCode = connection.getResponseCode();
            if (responseCode === 200) {
                var inputStream = connection.getInputStream();
                var response = "";
                var reader = new java.io.BufferedReader(new java.io.InputStreamReader(inputStream, "UTF-8"));
                var line;
                while ((line = reader.readLine()) !== null) {
                    response += line;
                }
                reader.close();
                
                var result = JSON.parse(response);
                if (result.summary) {
                    replier.reply("📝 YouTube 영상 요약:\n\n🎥 " + result.video_title + "\n\n" + result.summary);
                } else {
                    replier.reply("❌ 요약 생성 실패: " + (result.error || "알 수 없는 오류"));
                }
            } else {
                replier.reply("❌ 서버 오류 (HTTP " + responseCode + ")");
            }
            
        } catch (e) {
            // 더 자세한 오류 정보 제공
            var errorMsg = "❌ PC 서버 연결 실패\n";
            if (e.toString().includes("SocketTimeoutException")) {
                errorMsg += "⏰ 처리 시간이 너무 오래 걸립니다. 잠시 후 다시 시도해주세요.";
            } else if (e.toString().includes("ConnectException")) {
                errorMsg += "🔌 서버에 연결할 수 없습니다. PC 서버가 실행 중인지 확인해주세요.";
            } else {
                errorMsg += "오류: " + e.toString();
            }
            replier.reply(errorMsg);
        }
    }
}

// 아래는 수정할 필요 없는 기본 함수들입니다.
function onCreate(savedInstanceState, activity) {}
function onStart(activity) {}
function onResume(activity) {}
function onPause(activity) {}
function onStop(activity) {} 