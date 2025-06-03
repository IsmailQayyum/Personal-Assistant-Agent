import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';
import 'package:http/http.dart' as http;
import '../models/chat_message.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:8000';
  String? _sessionId;

  String? get sessionId => _sessionId;

  Future<ChatMessage> sendMessage(String message) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/chat'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'message': message,
          'session_id': _sessionId,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return ChatMessage(
          content: data['response'] ?? data['message'] ?? '',
          isUser: false,
          timestamp: DateTime.now(),
          sessionId: _sessionId,
        );
      } else {
        throw Exception('Failed to send message: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error sending message: $e');
    }
  }

  Future<bool> uploadDocument(File file) async {
    try {
      final request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/upload'),
      );

      request.files.add(
        await http.MultipartFile.fromPath(
          'file',
          file.path,
        ),
      );

      final response = await request.send();
      final responseData = await response.stream.bytesToString();
      final data = jsonDecode(responseData);

      if (response.statusCode == 200 && data['success'] == true) {
        return true;
      } else {
        throw Exception('Failed to upload document: ${data['error'] ?? response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error uploading document: $e');
    }
  }

  Future<bool> uploadDocumentWeb(Uint8List bytes, String fileName) async {
    try {
      final request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/upload'),
      );
      request.files.add(
        http.MultipartFile.fromBytes(
          'file',
          bytes,
          filename: fileName,
        ),
      );
      final response = await request.send();
      final responseData = await response.stream.bytesToString();
      final data = jsonDecode(responseData);

      if (response.statusCode == 200 && data['success'] == true) {
        return true;
      } else {
        throw Exception('Failed to upload document: ${data['error'] ?? response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error uploading document: $e');
    }
  }

  Future<List<ChatMessage>> getChatHistory() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/history'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => ChatMessage.fromJson(json)).toList();
      } else {
        throw Exception('Failed to get chat history: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error getting chat history: $e');
    }
  }

  void setSessionId(String sessionId) {
    _sessionId = sessionId;
  }
} 