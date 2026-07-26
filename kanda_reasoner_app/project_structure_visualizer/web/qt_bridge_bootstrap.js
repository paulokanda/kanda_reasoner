(function () {
  "use strict";

  const state = {
    bridge: null,
    connecting: false,
    timer: 0,
    deadline: 0,
    generationId: "",
    onConnected: null,
    onError: null
  };

  function fail(message) {
    state.connecting = false;
    if (state.timer) {
      window.clearTimeout(state.timer);
      state.timer = 0;
    }
    if (typeof state.onError === "function") {
      state.onError(String(message || "QWebChannel connection failed."));
    }
  }

  function finish(bridge) {
    state.bridge = bridge || null;
    state.connecting = false;
    if (state.timer) {
      window.clearTimeout(state.timer);
      state.timer = 0;
    }
    if (!state.bridge) {
      fail("QWebChannel did not expose projectGraphBridge.");
      return;
    }
    if (typeof state.onConnected === "function") {
      state.onConnected(state.bridge);
    }
  }

  function poll() {
    if (state.bridge) {
      finish(state.bridge);
      return;
    }
    const transportReady = Boolean(
      window.qt && window.qt.webChannelTransport
    );
    const libraryReady = typeof window.QWebChannel === "function";
    if (transportReady && libraryReady) {
      try {
        new window.QWebChannel(
          window.qt.webChannelTransport,
          function (channel) {
            finish(channel.objects.projectGraphBridge || null);
          }
        );
      } catch (error) {
        fail(error instanceof Error ? error.message : String(error));
      }
      return;
    }
    if (Date.now() >= state.deadline) {
      fail(
        "QWebChannel transport or library was not ready before timeout."
      );
      return;
    }
    state.timer = window.setTimeout(poll, 50);
  }

  function connect(generationId, onConnected, onError) {
    state.generationId = String(generationId || "");
    state.onConnected = onConnected;
    state.onError = onError;
    if (state.bridge) {
      finish(state.bridge);
      return true;
    }
    if (state.connecting) {
      return true;
    }
    state.connecting = true;
    state.deadline = Date.now() + 30000;
    poll();
    return true;
  }

  function notify(methodName, args) {
    if (!state.bridge || typeof state.bridge[methodName] !== "function") {
      return false;
    }
    state.bridge[methodName].apply(state.bridge, args || []);
    return true;
  }

  window.kandaQtBridge = {
    connect: connect,
    notify: notify,
    isConnected: function () { return Boolean(state.bridge); }
  };
}());
