class ChatMessage {
  final String content;
  final bool isUser;
  final DateTime timestamp;
  final String? sessionId;

  ChatMessage({
    required this.content,
    required this.isUser,
    required this.timestamp,
    this.sessionId,
  });

  factory ChatMessage.fromJson(Map<String, dynamic> json) {
    return ChatMessage(
      content: json['message'] ?? json['response'] ?? '',
      isUser: json['role'] == 'user',
      timestamp: DateTime.parse(json['timestamp'] ?? DateTime.now().toIso8601String()),
      sessionId: json['session_id'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'message': content,
      'role': isUser ? 'user' : 'assistant',
      'timestamp': timestamp.toIso8601String(),
      'session_id': sessionId,
    };
  }
} 