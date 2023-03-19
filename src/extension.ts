import * as vscode from 'vscode';
import WebSocket = require('ws');
const SERVER_URL = 'ws://localhost:8765';

async function activate(context: vscode.ExtensionContext) {
  let ws = new WebSocket(SERVER_URL);

  let disposable1 = vscode.commands.registerCommand('extension.sendCode', async () => {
    // ...
  });

  let disposable2 = vscode.commands.registerCommand('extension.requestModification', async () => {
    // ...
  });

  let disposable3 = vscode.commands.registerCommand('extension.reportError', async () => {
    // ...
  });

  let disposable4 = vscode.commands.registerCommand('extension.runCode', async () => {
    // ...
  });

  ws.on('message', async (data: WebSocket.Data) => {
    // ...
  });

  context.subscriptions.push(disposable1, disposable2, disposable3, disposable4);
}

exports.activate = activate;

function deactivate() {}

module.exports = {
  activate,
  deactivate
};
