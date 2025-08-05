const scriptName = "YouTube 요약 봇";

/**
 * YouTube URL을 감지하여 자막을 추출하고 AI로 요약하는 봇
 */
function response(room, msg, sender, isGroupChat, replier) {
    // YouTube URL 패턴 확인 (일반 영상, 라이브, 쇼츠 모두 포함)
    if (msg.includes("youtu.be/") || msg.includes("youtube.com/watch") || msg.includes("youtube.com/live/") || msg.includes("youtube.com/shorts/")) {
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
            var url = new java.net.URL("https://ytchoi.vercel.app/api/youtube");
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
            if (responseCode === 200 || responseCode === 400) {
                // 성공 응답(200) 또는 클라이언트 오류(400) 모두 JSON으로 처리
                var inputStream;
                if (responseCode === 200) {
                    inputStream = connection.getInputStream();
                } else {
                    inputStream = connection.getErrorStream();
                }
                
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
                } else if (result.error) {
                    // 자막이 없거나 다른 오류의 경우 친근한 메시지로 안내
                    if (result.error.includes("자막을 추출할 수 없습니다")) {
                        replier.reply("😔 죄송합니다. 이 영상은 자막이 없어서 요약할 수 없어요.\n\n📝 자막이 있는 영상을 올려주시면 요약해드릴게요!");
                    } else if (result.error.includes("요약을 생성할 수 없습니다")) {
                        replier.reply("😅 요약 생성 중 문제가 발생했어요. 잠시 후 다시 시도해주세요!");
                    } else {
                        replier.reply("❌ 처리 실패: " + result.error);
                    }
                } else {
                    replier.reply("❌ 알 수 없는 오류가 발생했습니다.");
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