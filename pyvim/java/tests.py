from .context import CompletionContext

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


test_get_position()
