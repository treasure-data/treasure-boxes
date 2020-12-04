/**
 * @ignore
 */
export default class {
    generateId() {
        const timestamp = (+new Date()).toString(36);
        const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        let result = '';
        for (let i = 0; i < 16; i++) {
            result += chars[Math.floor(Math.random() * chars.length)];
        }
        return `${timestamp}-${result}`;
    }

    readCookie(key) {
        const cookies = window.document.cookie || '';
        return (`; ${cookies};`.match(`; ${key}=([^\S;]*)`) || [])[1];
    }

    mergeObj(objArray) {
        let obj = {};
        for (let i = 0; i < objArray.length; i++) {
            for (let k in objArray[i]) {
                if (typeof objArray[i][k] === 'object' && objArray[i][k] !== null && !Array.isArray(objArray[i][k])) {
                    obj[k] = obj[k] ? this.mergeObj([obj[k], objArray[i][k]]) : objArray[i][k];
                } else if (Array.isArray(objArray[i][k])) {
                    obj[k] = obj[k] ? obj[k].concat(objArray[i][k]) : objArray[i][k];
                } else {
                    obj[k] = objArray[i][k];
                }
            }
        }
        return obj;
    }

    setSessionId(sessionOption = {}) {
        const sesCookie = this.readCookie('tdextSesId') || '';
        const sessionId = sesCookie.length > 8 ? sesCookie : sessionOption.rootId;
        const domain = sessionOption.domain ? ` Domain=${sessionOption.domain};` : '';
        const lifetime = sessionOption.lifetime ? ` Max-Age=${sessionOption.lifetime};` : '';
        window.document.cookie = `tdextSesId=${sessionId};Path=/;${domain}${lifetime}`;
        return sessionId;
    }

    getPerformanceInfo() {
        let timing = window.performance.timing,
            interactive = timing.domInteractive - timing.domLoading,
            dcl = timing.domContentLoadedEventStart - timing.domLoading,
            complete = timing.domComplete - timing.domLoading,
            since_dns = +new Date() - timing.domainLookupStart,
            since_req = +new Date() - timing.requestStart,
            since_dl = +new Date() - timing.domLoading;
        return {
            performance_interactive: interactive >= 0 ? interactive : undefined,
            performance_dcl: dcl >= 0 ? dcl : undefined,
            performance_complete: complete >= 0 ? complete : undefined,
            performance_ts_dns: since_dns >= 0 ? since_dns : undefined,
            performance_ts_req: since_req >= 0 ? since_req : undefined,
            performance_ts_dl: since_dl >= 0 ? since_dl : undefined,
        };
    }

    getMediaInfo(element) {
        if (element) {
            return {
                media_src: element.src,
                media_type: element.type || undefined,
                media_width: element.clientWidth || undefined,
                media_height: element.clientHeight || undefined,
                media_current_time: Math.round(element.currentTime * 10) / 10,
                media_duration: Math.round(element.duration * 10) / 10,
                media_played_percent: Math.round((element.currentTime / element.duration) * 1000) / 10,
                media_player_id: element.playerId || undefined,
                media_muted: element.muted || false,
                media_default_muted: element.defaultMuted || false,
                media_autoplay: element.autoplay || false,
                media_attr: element.dataset ? JSON.stringify(element.dataset) : undefined,
            };
        } else {
            return false;
        }
    }

    getFormStats(formDetail, targetEvent, targetElement, initTimestamp) {
        const elementName = targetElement.name || targetElement.id || '-';
        let valueLength = 0;
        if (targetElement.tagName.toLowerCase() === 'select') {
            for (let i = 0; i < targetElement.length; i++) {
                targetElement[i].selected ? valueLength++ : false;
            }
        } else if (
            targetElement.tagName.toLowerCase() === 'input' &&
            (targetElement.type === 'checkbox' || targetElement.type === 'radio')
        ) {
            valueLength = targetElement.checked ? 1 : 0;
        } else {
            valueLength = targetElement.value.length;
        }
        if (targetElement.type !== 'hidden') {
            formDetail.fmItems[elementName] = {
                status: targetEvent,
                length: valueLength,
            };
        }
        if (!formDetail.fmFirstItem) {
            formDetail.fmFirstItem = targetElement.name || targetElement.id || '-';
            formDetail.fmStartedSinceInitMs = +new Date() - initTimestamp;
        }
        formDetail.fmLastItem = targetElement.name || targetElement.id || '-';
        formDetail.fmEndedSinceInitMs = +new Date() - initTimestamp;
        formDetail.fmDurationMs = formDetail.fmEndedSinceInitMs - formDetail.fmStartedSinceInitMs;
        return formDetail;
    }

    getVisibility(targetElement, targetWindow) {
        let textLength = 0,
            targetRect = {};
        try {
            targetRect = targetElement.getBoundingClientRect();
            textLength = targetElement.innerText.length;
        } catch (e) {
            targetRect = {};
        }

        const viewportHeight = window[targetWindow].innerHeight;
        const documentHeight = window[targetWindow].document.documentElement.scrollHeight;
        const documentIsVisible = window[targetWindow].document.visibilityState || 'unknown';
        const documentVisibleTop =
            'pageYOffset' in window[targetWindow]
                ? window[targetWindow].pageYOffset
                : (
                      window[targetWindow].document.documentElement ||
                      window[targetWindow].document.body.parentNode ||
                      window[targetWindow].document.body
                  ).scrollTop;
        const documentVisibleBottom = documentVisibleTop + viewportHeight;
        const targetHeight = targetRect.height;
        const targetMarginTop = targetRect.top <= 0 ? 0 : targetRect.top;
        const targetMarginBottom =
            (targetRect.bottom - viewportHeight) * -1 <= 0 ? 0 : (targetRect.bottom - viewportHeight) * -1;
        const documentScrollUntil = documentVisibleBottom;
        const documentScrollRate = documentVisibleBottom / documentHeight;

        let targetVisibleTop = null,
            targetVisibleBottom = null,
            isInView = false;

        if (targetRect.top >= 0 && targetRect.bottom > viewportHeight && targetRect.top >= viewportHeight) {
            // pre
            targetVisibleTop = null;
            targetVisibleBottom = null;
            isInView = false;
        } else if (targetRect.top >= 0 && targetRect.bottom > viewportHeight && targetRect.top < viewportHeight) {
            // top
            targetVisibleTop = 0;
            targetVisibleBottom = viewportHeight - targetRect.top;
            isInView = true;
        } else if (targetRect.top < 0 && targetRect.bottom > viewportHeight) {
            // middle
            targetVisibleTop = targetRect.top * -1;
            targetVisibleBottom = targetVisibleTop + viewportHeight;
            isInView = true;
        } else if (targetRect.top >= 0 && targetRect.bottom <= viewportHeight) {
            // all in
            targetVisibleTop = 0;
            targetVisibleBottom = targetHeight;
            isInView = true;
        } else if (targetRect.top < 0 && targetRect.bottom >= 0 && targetRect.bottom <= viewportHeight) {
            // bottom
            targetVisibleTop = targetHeight + targetRect.top;
            targetVisibleBottom = targetHeight;
            isInView = true;
        } else if (targetRect.top < 0 && targetRect.bottom < 0) {
            // post
            targetVisibleTop = null;
            targetVisibleBottom = null;
            isInView = false;
        } else {
            isInView = false;
        }
        return {
            dHeight: documentHeight,
            dIsVisible: documentIsVisible,
            dVisibleTop: documentVisibleTop,
            dVisibleBottom: documentVisibleBottom,
            dScrollUntil: documentScrollUntil,
            dScrollRate: documentScrollRate,
            tHeight: targetHeight,
            tVisibleTop: targetVisibleTop,
            tVisibleBottom: targetVisibleBottom,
            tMarginTop: targetMarginTop,
            tMarginBottom: targetMarginBottom,
            tScrollUntil: targetVisibleBottom,
            tScrollRate: targetVisibleBottom / targetHeight,
            tViewableRate: (targetVisibleBottom - targetVisibleTop) / targetHeight,
            tIsInView: isInView,
            tLength: textLength,
        };
    }

    queryMatch(selector, target, targetFlag = false, targetWindow) {
        let element,
            category = 'button',
            p = [];
        if (target.nodeType === 3) {
            target = target.parentNode;
        }
        while (target && target !== window[targetWindow].document) {
            let matches = (
                target.matches ||
                target.msMatchesSelector ||
                function() {
                    return false;
                }
            ).bind(target);
            if (targetFlag) {
                if (target.hasAttribute(targetFlag)) {
                    p.unshift(target.getAttribute(targetFlag));
                }
            } else {
                let elm = target.tagName.toLowerCase();
                if (elm !== 'html' && elm !== 'body') {
                    if (target.id) {
                        elm += `.${target.id}`;
                    }
                    p.unshift(elm);
                }
            }

            if (!element && matches(selector)) {
                if (target.tagName.toLowerCase() === 'a') {
                    category = 'link';
                } else {
                    category = target.tagName.toLowerCase();
                }
                element = target;
            }
            target = target.parentNode;
        }
        if (element && p.length > 0) {
            return {
                element: element,
                category: category,
                path: p.join('>'),
            };
        } else {
            return false;
        }
    }
}
