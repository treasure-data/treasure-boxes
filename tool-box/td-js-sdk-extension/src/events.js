let managedEvents = {},
    handlerKey = 0;

/**
 * @ignore
 */
export default class {
    constructor(config) {
        let event, timer;

        try {
            event = new CustomEvent(config.eventName);
        } catch (e) {
            event = window[config.targetWindow].document.createEvent('CustomEvent');
            event.initCustomEvent(config.eventName, false, false, {});
        }

        window[config.targetWindow].requestAnimationFrame =
            window[config.targetWindow].requestAnimationFrame ||
            window[config.targetWindow].mozRequestAnimationFrame ||
            window[config.targetWindow].webkitRequestAnimationFrame;

        (function recurringEvent() {
            window[config.targetWindow].requestAnimationFrame(recurringEvent);
            if (timer) {
                return false;
            }
            timer = setTimeout(() => {
                window[config.targetWindow].dispatchEvent(event);
                timer = null;
            }, config.eventFrequency);
        })();
    }

    addListener(element, type, listener, capture) {
        element.addEventListener(type, listener, capture);
        managedEvents[handlerKey] = {
            element: element,
            type: type,
            listener: listener,
            capture: capture,
        };
        return handlerKey++;
    }

    removeListener(handlerKey) {
        if (handlerKey in managedEvents) {
            let event = managedEvents[handlerKey];
            event.element.removeEventListener(event.type, event.listener, event.capture);
        }
    }
}
