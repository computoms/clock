from ..task import Task
from ..task import Period
import datetime

def parse_singledescription_parsescorrectly():
    t = Task('this is a test', datetime.datetime.now())
    assert(t.description == 'this is a test')
    assert(len(t.tags) == 0)
    assert(len(t.periods) == 1)

def parse_descriptionwithonetags_parsetags():
    t = Task("this is a description with one +tag", datetime.datetime.now())
    assert(len(t.tags) == 1)
    assert(t.tags[0] == '+tag')

def parse_descriptionwithtwotags_parsetags():
    t = Task("this is a description with two +tag +tag2", datetime.datetime.now())
    assert(len(t.tags) == 2)
    assert(t.tags[1] == '+tag2')

def parse_withid_parseid():
    t = Task("test with id .4537", datetime.datetime.now())
    assert(len(t.ids) == 1)
    assert(t.ids[0] == '.4537')

def parse_withid_addsjiratag():
    t = Task("test with id .4537", datetime.datetime.now())
    assert(len(t.tags) == 1)
    assert(t.tags[0] == '+jira')

def parse_withid_removesidfromdescription():
    t = Task("test with id .4537", datetime.datetime.now())
    assert(t.description == 'test with id')

def parse_withnewline_removesnewline():
    t = Task("test with new line\n", datetime.datetime.now())
    assert(t.description == 'test with new line')

def parse_withcariagereturn_removesnewline():
    t = Task("test with new line\r", datetime.datetime.now())
    assert(t.description == 'test with new line')

def isstop_whenstop_returnstrue():
    t = Task('[Stop]', datetime.datetime.now())
    assert(t.is_stop())

def isstop_withspaces_returnstrue():
    t = Task(' [Stop]  ', datetime.datetime.now())
    assert(t.is_stop())

def isstop_notstop_returnsfalse():
    t = Task(' [Stop', datetime.datetime.now())
    assert(not t.is_stop())

def finish_noperiods_doesnotthrow():
    t = Task('test', datetime.datetime.now())
    t.periods = []
    t.finish(datetime.datetime.now())

def finish_onetask_finishestask():
    t = Task('test', datetime.datetime.now())
    t.finish(datetime.datetime.now())
    assert(len(t.periods) == 1)
    assert(t.periods[0].end.year != 1900)

def discardlast_noperiods_doesnotthrow():
    t = Task('test', datetime.datetime.now())
    t.periods = []
    t.discard_last()

def discardlast_oneperiod_clearsperiods():
    t = Task('test', datetime.datetime.now())
    t.discard_last()
    assert(len(t.periods) == 0)

def ismatching_notag_returnstrue():
    t = Task('test', datetime.datetime.now())
    assert(t.is_matching([]))

def ismatching_onetag_returnstrue():
    t = Task('test +cat', datetime.datetime.now())
    assert(t.is_matching(['+cat']))

def ismatching_onetagdifferent_returnsfalse():
    t = Task('test +cat', datetime.datetime.now())
    assert(not t.is_matching(['+test']))

def ismatching_twotags_returnstrue():
    t = Task('test +cat1 +cat2', datetime.datetime.now())
    assert(t.is_matching(['+cat1', '+cat2']))

def ismatching_twotagswrongorder_returnsfalse():
    t = Task('test +cat2 +cat1', datetime.datetime.now())
    assert(not t.is_matching(['+cat1', '+cat2']))

def ismatching_onetagtestingtwo_returnsfalse():
    t = Task('test +cat', datetime.datetime.now())
    assert(not t.is_matching(['+cat', '+cat2']))

def duration_total_empty_returnszero():
    t = Task('test', datetime.datetime.now())
    t.periods = []
    assert(t.duration_total().seconds == 0)

def duration_total_one_returnsone():
    t = Task('test', datetime.datetime(2022,1,1,10,0,0))
    t.finish(datetime.datetime(2022,1,1,11,0,0))
    assert(t.duration_total().seconds == 3600)

def duration_total_two_returnssum():
    t = Task('test', datetime.datetime(2022, 1, 1, 10, 0, 0))
    t.finish(datetime.datetime(2022, 1, 1, 10, 30, 0))
    p = Period(datetime.datetime(2022,1,1,12,0,0))
    p.end = datetime.datetime(2022, 1, 1, 12, 30, 0)
    t.periods.append(p)
    assert(t.duration_total().seconds == 3600)

def equals_differentdescription_returnsfalse():
    t = Task('test1', datetime.datetime.now())
    t2 = Task('test2', datetime.datetime.now())
    assert(not t.equals(t2))

def equals_differenttags_returnsfalse():
    t = Task('test +tag', datetime.datetime.now())
    t2 = Task('test', datetime.datetime.now())
    assert(not t.equals(t2))

def equals_areequal_returnstrue():
    t = Task('test +tag', datetime.datetime.now())
    t2 = Task('test +tag', datetime.datetime.now())
    assert(t.equals(t2))

def copyempty_nonemptytask_returnsemptytask():
    t = Task('test', datetime.datetime.now())
    assert(len(t.periods) != 0)
    t2 = t.copy_empty()
    assert(len(t2.periods) == 0)


def run():
    parse_singledescription_parsescorrectly()
    parse_descriptionwithonetags_parsetags()
    parse_descriptionwithtwotags_parsetags()
    parse_withid_parseid()
    parse_withid_addsjiratag()
    parse_withid_removesidfromdescription()
    parse_withnewline_removesnewline()
    parse_withcariagereturn_removesnewline()

    isstop_whenstop_returnstrue()
    isstop_withspaces_returnstrue()
    isstop_notstop_returnsfalse()

    finish_noperiods_doesnotthrow()
    finish_onetask_finishestask()

    discardlast_noperiods_doesnotthrow()
    discardlast_oneperiod_clearsperiods()

    ismatching_notag_returnstrue()
    ismatching_onetag_returnstrue()
    ismatching_onetagdifferent_returnsfalse()
    ismatching_twotags_returnstrue()
    ismatching_twotagswrongorder_returnsfalse()
    ismatching_onetagtestingtwo_returnsfalse()

    duration_total_empty_returnszero()
    duration_total_one_returnsone()
    duration_total_two_returnssum()

    equals_areequal_returnstrue()
    equals_differentdescription_returnsfalse()
    equals_differenttags_returnsfalse()

    copyempty_nonemptytask_returnsemptytask()