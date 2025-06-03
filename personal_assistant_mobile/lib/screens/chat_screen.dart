import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:uuid/uuid.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import '../models/chat_message.dart';
import '../services/api_service.dart';
import '../widgets/chat_bubble.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({Key? key}) : super(key: key);

  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final ApiService _apiService = ApiService();
  final TextEditingController _messageController = TextEditingController();
  final List<ChatMessage> _messages = [];
  bool _isLoading = false;
  String? _currentDocument;

  @override
  void initState() {
    super.initState();
    _initializeSession();
  }

  void _initializeSession() {
    final sessionId = const Uuid().v4();
    _apiService.setSessionId(sessionId);
  }

  Future<void> _handleFileUpload() async {
    try {
      final result = await FilePicker.platform.pickFiles(
        type: FileType.custom,
        allowedExtensions: ['txt', 'pdf'],
      );

      if (result != null) {
        setState(() => _isLoading = true);

        bool success = false;
        if (kIsWeb) {
          // On web, use bytes
          final bytes = result.files.single.bytes;
          final fileName = result.files.single.name;
          if (bytes != null) {
            success = await _apiService.uploadDocumentWeb(bytes, fileName);
          }
        } else {
          // On desktop/mobile, use path
          final file = File(result.files.single.path!);
          success = await _apiService.uploadDocument(file);
        }

        if (success) {
          setState(() {
            _currentDocument = result.files.single.name;
            _messages.add(ChatMessage(
              content: 'Document "${result.files.single.name}" has been loaded. You can now ask questions about its contents.',
              isUser: false,
              timestamp: DateTime.now(),
            ));
          });
        }
      }
    } catch (e) {
      _showError('Failed to upload document: $e');
    } finally {
      setState(() => _isLoading = false);
    }
  }

  Future<void> _sendMessage() async {
    final message = _messageController.text.trim();
    if (message.isEmpty) return;

    setState(() {
      _messages.add(ChatMessage(
        content: message,
        isUser: true,
        timestamp: DateTime.now(),
      ));
      _messageController.clear();
      _isLoading = true;
    });

    try {
      final response = await _apiService.sendMessage(message);
      setState(() {
        _messages.add(response);
      });
    } catch (e) {
      _showError('Failed to send message: $e');
    } finally {
      setState(() => _isLoading = false);
    }
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.red,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Assistant'),
        actions: [
          IconButton(
            icon: const Icon(Icons.upload_file),
            onPressed: _isLoading ? null : _handleFileUpload,
          ),
        ],
      ),
      body: Column(
        children: [
          if (_currentDocument != null)
            Container(
              padding: const EdgeInsets.all(8),
              color: Colors.blue.withOpacity(0.1),
              child: Row(
                children: [
                  const Icon(Icons.description, color: Colors.blue),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      'Current document: $_currentDocument',
                      style: const TextStyle(color: Colors.blue),
                    ),
                  ),
                ],
              ),
            ),
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(8),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                return ChatBubble(message: _messages[index]);
              },
            ),
          ),
          if (_isLoading)
            const Padding(
              padding: EdgeInsets.all(8.0),
              child: CircularProgressIndicator(),
            ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _messageController,
                    decoration: const InputDecoration(
                      hintText: 'Type your message...',
                      border: OutlineInputBorder(),
                    ),
                    onSubmitted: (_) => _sendMessage(),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton(
                  icon: const Icon(Icons.send),
                  onPressed: _isLoading ? null : _sendMessage,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _messageController.dispose();
    super.dispose();
  }
} 