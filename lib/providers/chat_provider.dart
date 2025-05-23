import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:file_picker/file_picker.dart';

class Message {
  final String content;
  final bool isUser;
  final DateTime timestamp;

  Message({
    required this.content,
    required this.isUser,
    required this.timestamp,
  });
}

class ChatProvider with ChangeNotifier {
  List<Message> _messages = [];
  bool _isLoading = false;
  String? _currentDocument;
  static const String baseUrl = 'http://localhost:8000';

  List<Message> get messages => _messages;
  bool get isLoading => _isLoading;
  String? get currentDocument => _currentDocument;

  Future<void> sendMessage(String message) async {
    _isLoading = true;
    notifyListeners();

    _messages.add(Message(
      content: message,
      isUser: true,
      timestamp: DateTime.now(),
    ));

    try {
      final response = await http.post(
        Uri.parse('$baseUrl/chat'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: jsonEncode({
          'messages': _messages.map((m) => {
            'role': m.isUser ? 'user' : 'assistant',
            'content': m.content,
          }).toList(),
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        _messages.add(Message(
          content: data['message'],
          isUser: false,
          timestamp: DateTime.now(),
        ));
      } else {
        String errorMessage = 'Error: Failed to get response';
        try {
          final errorData = jsonDecode(response.body);
          errorMessage = 'Error: ${errorData['detail'] ?? errorMessage}';
        } catch (e) {
          errorMessage = 'Error: Server returned ${response.statusCode}';
        }
        _messages.add(Message(
          content: errorMessage,
          isUser: false,
          timestamp: DateTime.now(),
        ));
      }
    } catch (e) {
      String errorMessage = 'Error: Failed to connect to server';
      if (e.toString().contains('Failed to fetch')) {
        errorMessage = 'Error: Cannot connect to server. Please make sure the server is running at $baseUrl';
      }
      _messages.add(Message(
        content: errorMessage,
        isUser: false,
        timestamp: DateTime.now(),
      ));
    }

    _isLoading = false;
    notifyListeners();
  }

  Future<void> uploadDocument() async {
    try {
      FilePickerResult? result = await FilePicker.platform.pickFiles(
        type: FileType.custom,
        allowedExtensions: ['pdf', 'docx'],
      );

      if (result != null) {
        _currentDocument = result.files.single.name;
        notifyListeners();
        
        // Here you would typically upload the file to your backend
        // For now, we'll just send a message about the document
        await sendMessage('I have uploaded a document: $_currentDocument');
      }
    } catch (e) {
      _messages.add(Message(
        content: 'Error uploading document: $e',
        isUser: false,
        timestamp: DateTime.now(),
      ));
      notifyListeners();
    }
  }
} 