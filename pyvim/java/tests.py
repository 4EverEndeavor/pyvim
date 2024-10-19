import re

from .context import CompletionContext
from .java_bones import JavapMatchers

def test_get_position():
    lines = [
        'public EscalateThreatCaseToAlarmWSResponse escalateThreatCaseToAlarm(',
        '       final EscalateThreatCaseToAlarmWSRequest request) throws Exception',
        '{',
        '   final RUUID orgUuid = _getOrgUuid();',
        '   EscalateThreatCaseToAlarmWSResponse response = new EscalateThreatCaseToAlarmWSResponse();',
        '   response.setError(false);',
        '   request.set']
    context = CompletionContext(lines, 6, 14)
    print('ran test')


test_get_position()


def test_constructor():
    line = '  public src.api.java.com.rhombus.cloud.bpm.api.FindGeoLocationForIpRequest();'
    ms = JavapMatchers()
    match = re.compile(ms.methodMatcher).fullmatch(line)
    assert match is not None
    
test_constructor()
