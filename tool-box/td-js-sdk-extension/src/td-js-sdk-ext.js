import Events from './events';
import Utils from './utils';

const extVersion = '0.1.8',
    initTimestamp = +new Date();

let config,
    targetWindow,
    tdNs,
    events,
    utils,
    unloadEvent,
    eventHandlerKeys = { media: [] },
    prevTimestamp = initTimestamp;

/**
 * @ignore
 */
export default class TDExt {
    constructor() {}

    /**
     * Initialize a page level variables.
     */
    init(configObj) {
        config = configObj;
        utils = new Utils();
        targetWindow = config.targetWindow || 'self';
        tdNs = config.tdNs || 'td';
        this.rootId = utils.generateId();

        if ('onbeforeunload' in window[targetWindow]) {
            unloadEvent = 'beforeunload';
        } else if ('onpagehide' in window[targetWindow]) {
            unloadEvent = 'pagehide';
        } else {
            unloadEvent = 'unload';
        }

        if (config.eventName && config.eventFrequency && typeof events === 'undefined') {
            events = new Events({
                eventName: config.eventName,
                eventFrequency: config.eventFrequency,
                targetWindow: targetWindow,
            });
        }

        if ('performance' in window[targetWindow]) {
            if (
                window[targetWindow].document.readyState === 'interactive' ||
                window[targetWindow].document.readyState === 'complete'
            ) {
                this.trackAction('rum', 'page', {});
            } else {
                this.trackPerformance();
            }
        }

        if (config.options) {
            if (config.options.session && config.options.session.enable) {
                this.sesId = utils.setSessionId({
                    rootId: this.rootId,
                    domain: config.options.session.domain,
                    lifetime: config.options.session.lifetime,
                });
            }

            if (config.options.unload && config.options.unload.enable) {
                this.trackUnload();
            }

            if (config.options.scroll && config.options.scroll.enable) {
                this.trackScroll();
            }

            if (config.options.read && config.options.read.enable) {
                this.trackRead(config.options.read.target);
            }

            if (config.options.clicks && config.options.clicks.enable) {
                this.trackClicks();
            }

            if (config.options.media && config.options.media.enable) {
                this.trackMedia();
            }
        }
    }

    /**
     * Send a payload to TD endpoint.
     *
     */
    trackAction(action = 'unknown', category = 'unknown', context = {}, successCallback, failureCallback) {
        const now = +new Date(),
            mandatory = {
                action: action,
                category: category,
                root_id: this.rootId,
                ses_id: this.sesId,
                ext_version: extVersion,
                since_init_ms: now - initTimestamp,
                since_prev_ms: now - prevTimestamp,
            },
            payload = utils.mergeObj([mandatory, context, utils.getPerformanceInfo()]);
        prevTimestamp = now;
        window[targetWindow][tdNs].trackEvent(config.table, payload, successCallback, failureCallback);
    }

    trackPageview(context = {}, successCallback, failureCallback) {
        this.trackAction('view', 'page', context, successCallback, failureCallback);
    }

    /**
     * Add a tracker to the onload event.
     */
    trackPerformance() {
        events.removeListener(eventHandlerKeys['performance']);
        eventHandlerKeys['performance'] = events.addListener(
            window[targetWindow].document,
            'DOMContentLoaded',
            () => {
                this.trackAction('rum', 'page', {});
            },
            false
        );
    }

    /**
     * Add a tracker to the unload event.
     */
    trackUnload() {
        events.removeListener(eventHandlerKeys['unload']);
        eventHandlerKeys['unload'] = events.addListener(
            window[targetWindow],
            unloadEvent,
            () => {
                this.trackAction('unload', 'page', {});
            },
            false
        );
    }

    /**
     * Add a tracker to the click event.
     */
    trackClicks() {
        events.removeListener(eventHandlerKeys['click']);
        eventHandlerKeys['click'] = events.addListener(
            window[targetWindow].document.body,
            'click',
            clickEvent => {
                const targetAttribute = config.options.clicks.targetAttr || false;
                const trackableElement = utils.queryMatch(
                    'a, button, input, [role="button"]',
                    clickEvent.target,
                    targetAttribute,
                    targetWindow
                );
                let element = null;
                if (trackableElement) {
                    element = trackableElement.element;
                    this.trackAction('click', trackableElement.category, {
                        click_tag: element.tagName,
                        click_id: element.id || undefined,
                        click_class: element.className || undefined,
                        click_path: trackableElement.path || undefined,
                        click_link: element.href || undefined,
                        click_text: element.innerText || element.value || undefined,
                        click_attr: element.dataset ? JSON.stringify(element.dataset) : undefined,
                    });
                }
            },
            false
        );
    }

    /**
     * Start scroll observation by using custom event
     */
    trackScroll() {
        const each = config.options.scroll.granularity || 20;
        const steps = 100 / each;
        const limit = config.options.scroll.threshold * 1000 || 2 * 1000;
        let result = {},
            currentVal = 0,
            prevVal = 0,
            scrollUnit = 'percent';
        events.removeListener(eventHandlerKeys['scroll']);
        eventHandlerKeys['scroll'] = events.addListener(
            window[targetWindow],
            config.eventName,
            () => {
                result = utils.getVisibility(null, targetWindow);
                if (result.dIsVisible !== 'hidden' && result.dIsVisible !== 'prerender') {
                    if (config.options.scroll.unit === 'percent') {
                        currentVal = Math.floor(result.dScrollRate * steps) * each;
                    } else {
                        currentVal = result.dScrollUntil;
                        scrollUnit = 'pixel';
                    }

                    if (
                        (scrollUnit === 'percent' && currentVal > prevVal && currentVal >= 0 && currentVal <= 100) ||
                        (scrollUnit === 'pixel' && currentVal > prevVal && currentVal >= each)
                    ) {
                        setTimeout(() => {
                            if (currentVal > prevVal) {
                                this.trackAction('scroll', 'page', {
                                    page_height: result.dHeight,
                                    scroll_depth: currentVal,
                                    scroll_unit: scrollUnit,
                                });
                                prevVal = scrollUnit === 'percent' ? currentVal : currentVal + each;
                            }
                        }, limit);
                    }
                }
            },
            false
        );
    }

    /**
     * Start Read-Through Rate observation by using custom event
     * @param  {Element} target A target element to be observed for Read-Through.
     */
    trackRead(target) {
        if (!target) {
            return;
        }
        const each = config.options.read.granularity || 20;
        const steps = 100 / each;
        const limit = config.options.read.threshold * 1000 || 2 * 1000;
        const start = +new Date();
        let result, currentVal, prevVal;
        events.removeListener(eventHandlerKeys['read']);
        eventHandlerKeys['read'] = events.addListener(
            window[targetWindow],
            config.eventName,
            () => {
                currentVal = currentVal || 0;
                prevVal = prevVal || 0;
                result = utils.getVisibility(target, targetWindow);
                if (result.dIsVisible !== 'hidden' && result.dIsVisible !== 'prerender' && result.tIsInView) {
                    currentVal = Math.floor(result.tScrollRate * steps) * each;
                    if (currentVal > prevVal && currentVal >= 0 && currentVal <= 100) {
                        setTimeout(() => {
                            if (currentVal > prevVal && target) {
                                this.trackAction('read', 'content', {
                                    read_id: target.id || undefined,
                                    read_start_with: target.innerText.substring(0, 12) || undefined,
                                    read_target_height: result.tHeight,
                                    read_text_length: result.tLength,
                                    read_rate: currentVal,
                                    read_attr: target.dataset ? JSON.stringify(target.dataset) : undefined,
                                    read_elapsed_ms: +new Date() - start,
                                });
                                prevVal = currentVal;
                            }
                        }, limit);
                    }
                }
            },
            false
        );
    }

    /**
     * Set eventListeners for Media Tracking
     */
    trackMedia() {
        const targetEvents = ['play', 'pause', 'ended'];
        const heartbeat = config.options.media.heartbeat || 5;
        let flags = {};
        for (let i = 0; i < targetEvents.length; i++) {
            events.removeListener(eventHandlerKeys['media'][targetEvents[i]]);
            eventHandlerKeys['media'][targetEvents[i]] = events.addListener(
                window[targetWindow].document.body,
                targetEvents[i],
                event => {
                    this.trackAction(event.type, event.target.tagName.toLowerCase(), utils.getMediaInfo(event.target));
                },
                { capture: true }
            );
        }

        events.removeListener(eventHandlerKeys['media']['timeupdate']);
        eventHandlerKeys['media']['timeupdate'] = events.addListener(
            window[targetWindow].document,
            'timeupdate',
            event => {
                if (flags[event.target.src]) {
                    return false;
                }
                flags[event.target.src] = setTimeout(() => {
                    if (event.target.paused !== true && event.target.ended !== true) {
                        this.trackAction(
                            event.type,
                            event.target.tagName.toLowerCase(),
                            utils.getMediaInfo(event.target)
                        );
                    }
                    flags[event.target.src] = false;
                }, heartbeat * 1000);
            },
            { capture: true }
        );
    }

    /**
     * Measure stats for form completion
     */
    trackForm() {
        if (!this.trackFormTargets || this.trackFormTargets.length === 0) {
            return;
        }
        const targetEvents = ['focus', 'change'];
        for (let i = 0; i < this.trackFormTargets.length; i++) {
            let formDetail = {
                form_name: this.trackFormTargets[i].name || this.trackFormTargets[i].id || '-',
                form_attr: this.trackFormTargets[i].dataset,
                form_items: {},
            };
            for (let j = 0; j < targetEvents.length; j++) {
                events.removeListener(eventHandlerKeys['form'][targetEvents[j]]);
                eventHandlerKeys['form'][targetEvents[j]] = events.addListener(
                    this.trackFormTargets[i],
                    targetEvents[j],
                    event => {
                        formDetail = utils.getFormStats(formDetail, targetEvents[j], event.target, initTimestamp);
                    },
                    true
                );
            }
            events.removeListener(eventHandlerKeys['unload']);
            eventHandlerKeys['unload'] = events.addListener(
                window[targetWindow],
                unloadEvent,
                () => {
                    this.trackAction('stats', 'form', formDetail);
                },
                false
            );
        }
    }
}
