# THIS IS AN AUTOMATICALLY GENERATED FILE
# DO NOT EDIT!
# The template can be found in tools/hektemplate.py

from datetime import datetime
from sunpy.net import attr
from sunpy.util.util import anytim

class _ParamAttr(attr.Attr):
    def __init__(self, name, op, value):
        attr.Attr.__init__(self)
        self.name = name
        self.op = op
        self.value = value
    
    def collides(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.op == other.op and self.name == other.name


class _BoolParamAttr(_ParamAttr):
    def __init__(self, name, value='true'):
        _ParamAttr.__init__(self, name, '=', value)
    
    def __neg__(self):
        if self.value == 'true':
            return _BoolParamAttr(self.name, 'false')
        else:
            return _BoolParamAttr(self.name)
    
    def __pos__(self):
        return _BoolParamAttr(self.name)


class _ListAttr(attr.Attr):
    def __init__(self, key, item):
        attr.Attr.__init__(self)
        
        self.key = key
        self.item = item
    
    def collides(self, other):
        return False
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return vars(self) == vars(other)
    
    def __hash__(self):
        return hash(tuple(vars(self).itervalues()))


class EventType(_ListAttr):
    def __init__(self, item):
        _ListAttr.__init__(self, 'event_type', item)


class Time(attr.Attr):
    def __init__(self, start, end):
        attr.Attr.__init__(self)
        self.start = start
        self.end = end
    
    def collides(self, other):
        return isinstance(other, Time)
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return vars(self) == vars(other)
    
    def __hash__(self):
        return hash(tuple(vars(self).itervalues()))
    
    @classmethod
    def dt(cls, start, end):
        return cls(datetime(*start), datetime(*end))


# pylint: disable=R0913
class SpartialRegion(attr.Attr):
    def __init__(
        self, x1=-1200, y1=-1200, x2=1200, y2=1200, sys='helioprojective'):
        attr.Attr.__init__(self)
        
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.sys = sys
    
    def collides(self, other):
        return isinstance(other, SpartialRegion)
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return vars(self) == vars(other)
    
    def __hash__(self):
        return hash(tuple(vars(self).itervalues()))


class Contains(attr.Attr):
    def __init__(self, *types):
        attr.Attr.__init__(self)
        self.types = types
    
    def collides(self, other):
        return False
    
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return vars(self) == vars(other)
    
    def __hash__(self):
        return hash(tuple(vars(self).itervalues()))


class ComparisonParamAttrWrapper(object):
    def __init__(self, name):
        self.name = name
    
    def __lt__(self, other):
        return _ParamAttr(self.name, '<', other)
    
    def __le__(self, other):
        return _ParamAttr(self.name, '<=', other)
    
    def __gt__(self, other):
        return _ParamAttr(self.name, '>', other)
    
    def __ge__(self, other):
        return _ParamAttr(self.name, '>=', other)
    
    def __eq__(self, other):
        return _ParamAttr(self.name, '=', other)
    
    def __neq__(self, other):
        return _ParamAttr(self.name, '!=', other)


class _StringParamAttrWrapper(ComparisonParamAttrWrapper):
    def like(self, other):
        return _ParamAttr(self.name, 'like', other)


class _NumberParamAttrWrapper(ComparisonParamAttrWrapper):
    pass


walker = attr.AttrWalker()

@walker.add_applier(Contains)
# pylint: disable=E0102,C0103,W0613
def _a(wlk, root, state, dct):
    dct['type'] = 'contains'
    if not Contains in state:
        state[Contains] = 1
    
    nid = state[Contains]
    n = 0
    for n, type_ in enumerate(root.types):
        dct['event_type%d' % (nid + n)] = type_
    state[Contains] += n
    return dct

@walker.add_creator(
    Time, SpartialRegion, _ListAttr, _ParamAttr, attr.AttrAnd, Contains)
# pylint: disable=E0102,C0103,W0613
def _c(wlk, root, state):
    value = {}
    wlk.apply(root, state, value)
    return [value]

@walker.add_applier(Time)
# pylint: disable=E0102,C0103,W0613
def _a(wlk, root, state, dct):
    dct['event_starttime'] = anytim(root.start).strftime('%Y-%m-%dT%H:%M:%S')
    dct['event_endtime'] = anytim(root.end).strftime('%Y-%m-%dT%H:%M:%S')
    return dct

@walker.add_applier(SpartialRegion)
# pylint: disable=E0102,C0103,W0613
def _a(wlk, root, state, dct):
    dct['x1'] = root.x1
    dct['y1'] = root.y1
    dct['x2'] = root.x2
    dct['y2'] = root.y2
    dct['event_coordsys'] = root.sys
    return dct

@walker.add_applier(_ListAttr)
# pylint: disable=E0102,C0103,W0613
def _a(wlk, root, state, dct):
    if root.key in dct:
        dct[root.key] += ',%s' % root.item
    else:
        dct[root.key] = root.item
    return dct

@walker.add_applier(EventType)
# pylint: disable=E0102,C0103,W0613
def _a(wlk, root, state, dct):
    if dct.get('type', None) == 'contains':
        raise ValueError
    
    return wlk.super_apply(super(EventType, root), state, dct)

@walker.add_applier(_ParamAttr)
# pylint: disable=E0102,C0103,W0613
def _a(wlk, root, state, dct):
    if not _ParamAttr in state:
        state[_ParamAttr] = 0
    
    nid = state[_ParamAttr]
    dct['param%d' % nid] = root.name
    dct['op%d' % nid] = root.op
    dct['value%d' % nid] = root.value
    state[_ParamAttr] += 1
    return dct

@walker.add_applier(attr.AttrAnd)
# pylint: disable=E0102,C0103,W0613
def _a(wlk, root, state, dct):
    for attribute in root.attrs:
        wlk.apply(attribute, state, dct)

@walker.add_creator(attr.AttrOr)
# pylint: disable=E0102,C0103,W0613
def _c(wlk, root, state):
    blocks = []
    for attribute in root.attrs:
        blocks.extend(wlk.create(attribute, state))
    return blocks

@walker.add_creator(attr.DummyAttr)
# pylint: disable=E0102,C0103,W0613
def _c(wlk, root, state):
    return {}

@walker.add_applier(attr.DummyAttr)
# pylint: disable=E0102,C0103,W0613
def _a(wlk, root, state, dct):
    pass


@apply
class AR(_ListAttr):
    CompactnessCls = _StringParamAttrWrapper('AR_CompactnessCls')
    IntensKurt = _StringParamAttrWrapper('AR_IntensKurt')
    IntensMax = _StringParamAttrWrapper('AR_IntensMax')
    IntensMean = _StringParamAttrWrapper('AR_IntensMean')
    IntensMin = _StringParamAttrWrapper('AR_IntensMin')
    IntensSkew = _StringParamAttrWrapper('AR_IntensSkew')
    IntensTotal = _StringParamAttrWrapper('AR_IntensTotal')
    IntensUnit = _StringParamAttrWrapper('AR_IntensUnit')
    IntensVar = _StringParamAttrWrapper('AR_IntensVar')
    McIntoshCls = _StringParamAttrWrapper('AR_McIntoshCls')
    MtWilsonCls = _StringParamAttrWrapper('AR_MtWilsonCls')
    NOAANum = _StringParamAttrWrapper('AR_NOAANum')
    NOAAclass = _StringParamAttrWrapper('AR_NOAAclass')
    NumSpots = _StringParamAttrWrapper('AR_NumSpots')
    PenumbraCls = _StringParamAttrWrapper('AR_PenumbraCls')
    Polarity = _StringParamAttrWrapper('AR_Polarity')
    SpotAreaRaw = _StringParamAttrWrapper('AR_SpotAreaRaw')
    SpotAreaRawUncert = _StringParamAttrWrapper('AR_SpotAreaRawUncert')
    SpotAreaRawUnit = _StringParamAttrWrapper('AR_SpotAreaRawUnit')
    SpotAreaRepr = _StringParamAttrWrapper('AR_SpotAreaRepr')
    SpotAreaReprUncert = _StringParamAttrWrapper('AR_SpotAreaReprUncert')
    SpotAreaReprUnit = _StringParamAttrWrapper('AR_SpotAreaReprUnit')
    ZurichCls = _StringParamAttrWrapper('AR_ZurichCls')
    def __init__(self):
            _ListAttr.__init__(self, "event_type", 'ar')

@apply
class CE(_ListAttr):
    Accel = _StringParamAttrWrapper('CME_Accel')
    AccelUncert = _StringParamAttrWrapper('CME_AccelUncert')
    AccelUnit = _StringParamAttrWrapper('CME_AccelUnit')
    AngularWidth = _StringParamAttrWrapper('CME_AngularWidth')
    AngularWidthUnit = _StringParamAttrWrapper('CME_AngularWidthUnit')
    Mass = _StringParamAttrWrapper('CME_Mass')
    MassUncert = _StringParamAttrWrapper('CME_MassUncert')
    MassUnit = _StringParamAttrWrapper('CME_MassUnit')
    RadialLinVel = _StringParamAttrWrapper('CME_RadialLinVel')
    RadialLinVelMax = _StringParamAttrWrapper('CME_RadialLinVelMax')
    RadialLinVelMin = _StringParamAttrWrapper('CME_RadialLinVelMin')
    RadialLinVelStddev = _StringParamAttrWrapper('CME_RadialLinVelStddev')
    RadialLinVelUncert = _StringParamAttrWrapper('CME_RadialLinVelUncert')
    RadialLinVelUnit = _StringParamAttrWrapper('CME_RadialLinVelUnit')
    def __init__(self):
            _ListAttr.__init__(self, "event_type", 'ce')

@apply
class CD(_ListAttr):
    Area = _StringParamAttrWrapper('CD_Area')
    AreaUncert = _StringParamAttrWrapper('CD_AreaUncert')
    AreaUnit = _StringParamAttrWrapper('CD_AreaUnit')
    Mass = _StringParamAttrWrapper('CD_Mass')
    MassUncert = _StringParamAttrWrapper('CD_MassUncert')
    MassUnit = _StringParamAttrWrapper('CD_MassUnit')
    Volume = _StringParamAttrWrapper('CD_Volume')
    VolumeUncert = _StringParamAttrWrapper('CD_VolumeUncert')
    VolumeUnit = _StringParamAttrWrapper('CD_VolumeUnit')
    def __init__(self):
            _ListAttr.__init__(self, "event_type", 'cd')

CH = _ListAttr("event_type", 'ch')

CW = _ListAttr("event_type", 'cw')

@apply
class FI(_ListAttr):
    BarbsL = _StringParamAttrWrapper('FI_BarbsL')
    BarbsR = _StringParamAttrWrapper('FI_BarbsR')
    BarbsTot = _StringParamAttrWrapper('FI_BarbsTot')
    Chirality = _StringParamAttrWrapper('FI_Chirality')
    Length = _StringParamAttrWrapper('FI_Length')
    LengthUnit = _StringParamAttrWrapper('FI_LengthUnit')
    Tilt = _StringParamAttrWrapper('FI_Tilt')
    def __init__(self):
            _ListAttr.__init__(self, "event_type", 'fi')

FE = _ListAttr("event_type", 'fe')

FA = _ListAttr("event_type", 'fa')

@apply
class FL(_ListAttr):
    EFoldTime = _StringParamAttrWrapper('FL_EFoldTime')
    EFoldTimeUnit = _StringParamAttrWrapper('FL_EFoldTimeUnit')
    Fluence = _StringParamAttrWrapper('FL_Fluence')
    FluenceUnit = _StringParamAttrWrapper('FL_FluenceUnit')
    GOESCls = _StringParamAttrWrapper('FL_GOESCls')
    PeakEM = _StringParamAttrWrapper('FL_PeakEM')
    PeakEMUnit = _StringParamAttrWrapper('FL_PeakEMUnit')
    PeakFlux = _StringParamAttrWrapper('FL_PeakFlux')
    PeakFluxUnit = _StringParamAttrWrapper('FL_PeakFluxUnit')
    PeakTemp = _StringParamAttrWrapper('FL_PeakTemp')
    PeakTempUnit = _StringParamAttrWrapper('FL_PeakTempUnit')
    def __init__(self):
            _ListAttr.__init__(self, "event_type", 'fl')

LP = _ListAttr("event_type", 'lp')

OS = _ListAttr("event_type", 'os')

@apply
class SS(_ListAttr):
    SpinRate = _StringParamAttrWrapper('SS_SpinRate')
    SpinRateUnit = _StringParamAttrWrapper('SS_SpinRateUnit')
    def __init__(self):
            _ListAttr.__init__(self, "event_type", 'ss')

@apply
class EF(_ListAttr):
    AspectRatio = _StringParamAttrWrapper('EF_AspectRatio')
    AxisLength = _StringParamAttrWrapper('EF_AxisLength')
    AxisOrientation = _StringParamAttrWrapper('EF_AxisOrientation')
    AxisOrientationUnit = _StringParamAttrWrapper('EF_AxisOrientationUnit')
    FluxUnit = _StringParamAttrWrapper('EF_FluxUnit')
    LengthUnit = _StringParamAttrWrapper('EF_LengthUnit')
    NegEquivRadius = _StringParamAttrWrapper('EF_NegEquivRadius')
    NegPeakFluxOnsetRate = _StringParamAttrWrapper('EF_NegPeakFluxOnsetRate')
    OnsetRateUnit = _StringParamAttrWrapper('EF_OnsetRateUnit')
    PosEquivRadius = _StringParamAttrWrapper('EF_PosEquivRadius')
    PosPeakFluxOnsetRate = _StringParamAttrWrapper('EF_PosPeakFluxOnsetRate')
    ProximityRatio = _StringParamAttrWrapper('EF_ProximityRatio')
    SumNegSignedFlux = _StringParamAttrWrapper('EF_SumNegSignedFlux')
    SumPosSignedFlux = _StringParamAttrWrapper('EF_SumPosSignedFlux')
    def __init__(self):
            _ListAttr.__init__(self, "event_type", 'ef')

CJ = _ListAttr("event_type", 'cj')

PG = _ListAttr("event_type", 'pg')

OT = _ListAttr("event_type", 'ot')

NR = _ListAttr("event_type", 'nr')

@apply
class SG(_ListAttr):
    AspectRatio = _StringParamAttrWrapper('SG_AspectRatio')
    Chirality = _StringParamAttrWrapper('SG_Chirality')
    MeanContrast = _StringParamAttrWrapper('SG_MeanContrast')
    Orientation = _StringParamAttrWrapper('SG_Orientation')
    PeakContrast = _StringParamAttrWrapper('SG_PeakContrast')
    Shape = _StringParamAttrWrapper('SG_Shape')
    def __init__(self):
            _ListAttr.__init__(self, "event_type", 'sg')

SP = _ListAttr("event_type", 'sp')

CR = _ListAttr("event_type", 'cr')

@apply
class CC(_ListAttr):
    AxisUnit = _StringParamAttrWrapper('CC_AxisUnit')
    MajorAxis = _StringParamAttrWrapper('CC_MajorAxis')
    MinorAxis = _StringParamAttrWrapper('CC_MinorAxis')
    TiltAngleMajorFromRadial = _StringParamAttrWrapper('CC_TiltAngleMajorFromRadial')
    TiltAngleUnit = _StringParamAttrWrapper('CC_TiltAngleUnit')
    def __init__(self):
            _ListAttr.__init__(self, "event_type", 'cc')

ER = _ListAttr("event_type", 'er')

@apply
class TO(_ListAttr):
    Shape = _StringParamAttrWrapper('TO_Shape')
    def __init__(self):
            _ListAttr.__init__(self, "event_type", 'to')

@apply
class Wave(object):
    DisplMaxAmpl = _StringParamAttrWrapper('WaveDisplMaxAmpl')
    DisplMinAmpl = _StringParamAttrWrapper('WaveDisplMinAmpl')
    DisplUnit = _StringParamAttrWrapper('WaveDisplUnit')
    lMaxPower = _StringParamAttrWrapper('WavelMaxPower')
    lMaxPowerUncert = _StringParamAttrWrapper('WavelMaxPowerUncert')
    lMaxRange = _StringParamAttrWrapper('WavelMaxRange')
    lMinRange = _StringParamAttrWrapper('WavelMinRange')
    lUnit = _StringParamAttrWrapper('WavelUnit')


@apply
class Veloc(object):
    MaxAmpl = _StringParamAttrWrapper('VelocMaxAmpl')
    MaxPower = _StringParamAttrWrapper('VelocMaxPower')
    MaxPowerUncert = _StringParamAttrWrapper('VelocMaxPowerUncert')
    MinAmpl = _StringParamAttrWrapper('VelocMinAmpl')
    Unit = _StringParamAttrWrapper('VelocUnit')


@apply
class Freq(object):
    MaxRange = _StringParamAttrWrapper('FreqMaxRange')
    MinRange = _StringParamAttrWrapper('FreqMinRange')
    PeakPower = _StringParamAttrWrapper('FreqPeakPower')
    Unit = _StringParamAttrWrapper('FreqUnit')


@apply
class Intens(object):
    MaxAmpl = _StringParamAttrWrapper('IntensMaxAmpl')
    MinAmpl = _StringParamAttrWrapper('IntensMinAmpl')
    Unit = _StringParamAttrWrapper('IntensUnit')


@apply
class Area(object):
    AtDiskCenter = _StringParamAttrWrapper('Area_AtDiskCenter')
    AtDiskCenterUncert = _StringParamAttrWrapper('Area_AtDiskCenterUncert')
    Raw = _StringParamAttrWrapper('Area_Raw')
    Uncert = _StringParamAttrWrapper('Area_Uncert')
    Unit = _StringParamAttrWrapper('Area_Unit')


@apply
class BoundBox(object):
    C1LL = _StringParamAttrWrapper('BoundBox_C1LL')
    C1UR = _StringParamAttrWrapper('BoundBox_C1UR')
    C2LL = _StringParamAttrWrapper('BoundBox_C2LL')
    C2UR = _StringParamAttrWrapper('BoundBox_C2UR')


@apply
class Bound(object):
    ox_C1LL = _StringParamAttrWrapper('BoundBox_C1LL')
    ox_C1UR = _StringParamAttrWrapper('BoundBox_C1UR')
    ox_C2LL = _StringParamAttrWrapper('BoundBox_C2LL')
    ox_C2UR = _StringParamAttrWrapper('BoundBox_C2UR')
    CCNsteps = _StringParamAttrWrapper('Bound_CCNsteps')
    CCStartC1 = _StringParamAttrWrapper('Bound_CCStartC1')
    CCStartC2 = _StringParamAttrWrapper('Bound_CCStartC2')


@apply
class OBS(object):
    ChannelID = _StringParamAttrWrapper('OBS_ChannelID')
    DataPrepURL = _StringParamAttrWrapper('OBS_DataPrepURL')
    FirstProcessingDate = _StringParamAttrWrapper('OBS_FirstProcessingDate')
    IncludesNRT = _StringParamAttrWrapper('OBS_IncludesNRT')
    Instrument = _StringParamAttrWrapper('OBS_Instrument')
    LastProcessingDate = _StringParamAttrWrapper('OBS_LastProcessingDate')
    LevelNum = _StringParamAttrWrapper('OBS_LevelNum')
    MeanWavel = _StringParamAttrWrapper('OBS_MeanWavel')
    Observatory = _StringParamAttrWrapper('OBS_Observatory')
    Title = _StringParamAttrWrapper('OBS_Title')
    WavelUnit = _StringParamAttrWrapper('OBS_WavelUnit')


@apply
class Skel(object):
    Curvature = _StringParamAttrWrapper('Skel_Curvature')
    Nsteps = _StringParamAttrWrapper('Skel_Nsteps')
    StartC1 = _StringParamAttrWrapper('Skel_StartC1')
    StartC2 = _StringParamAttrWrapper('Skel_StartC2')


@apply
class FRM(object):
    Contact = _StringParamAttrWrapper('FRM_Contact')
    HumanFlag = _StringParamAttrWrapper('FRM_HumanFlag')
    Identifier = _StringParamAttrWrapper('FRM_Identifier')
    Institute = _StringParamAttrWrapper('FRM_Institute')
    Name = _StringParamAttrWrapper('FRM_Name')
    ParamSet = _StringParamAttrWrapper('FRM_ParamSet')
    SpecificID = _StringParamAttrWrapper('FRM_SpecificID')
    URL = _StringParamAttrWrapper('FRM_URL')
    VersionNumber = _StringParamAttrWrapper('FRM_VersionNumber')


@apply
class Event(object):
    C1Error = _StringParamAttrWrapper('Event_C1Error')
    C2Error = _StringParamAttrWrapper('Event_C2Error')
    ClippedSpatial = _StringParamAttrWrapper('Event_ClippedSpatial')
    ClippedTemporal = _StringParamAttrWrapper('Event_ClippedTemporal')
    Coord1 = _StringParamAttrWrapper('Event_Coord1')
    Coord2 = _StringParamAttrWrapper('Event_Coord2')
    Coord3 = _StringParamAttrWrapper('Event_Coord3')
    CoordSys = _StringParamAttrWrapper('Event_CoordSys')
    CoordUnit = _StringParamAttrWrapper('Event_CoordUnit')
    MapURL = _StringParamAttrWrapper('Event_MapURL')
    MaskURL = _StringParamAttrWrapper('Event_MaskURL')
    Npixels = _StringParamAttrWrapper('Event_Npixels')
    PixelUnit = _StringParamAttrWrapper('Event_PixelUnit')
    Probability = _StringParamAttrWrapper('Event_Probability')
    TestFlag = _StringParamAttrWrapper('Event_TestFlag')
    Type = _StringParamAttrWrapper('Event_Type')


@apply
class Outflow(object):
    Length = _StringParamAttrWrapper('Outflow_Length')
    LengthUnit = _StringParamAttrWrapper('Outflow_LengthUnit')
    OpeningAngle = _StringParamAttrWrapper('Outflow_OpeningAngle')
    Speed = _StringParamAttrWrapper('Outflow_Speed')
    SpeedUnit = _StringParamAttrWrapper('Outflow_SpeedUnit')
    TransSpeed = _StringParamAttrWrapper('Outflow_TransSpeed')
    Width = _StringParamAttrWrapper('Outflow_Width')
    WidthUnit = _StringParamAttrWrapper('Outflow_WidthUnit')


class Misc(object):
    KB_Archivist = _StringParamAttrWrapper('KB_Archivist')
    MaxMagFieldStrength = _StringParamAttrWrapper('MaxMagFieldStrength')
    MaxMagFieldStrengthUnit = _StringParamAttrWrapper('MaxMagFieldStrengthUnit')
    OscillNPeriods = _StringParamAttrWrapper('OscillNPeriods')
    OscillNPeriodsUncert = _StringParamAttrWrapper('OscillNPeriodsUncert')
    PeakPower = _StringParamAttrWrapper('PeakPower')
    PeakPowerUnit = _StringParamAttrWrapper('PeakPowerUnit')
    RasterScanType = _StringParamAttrWrapper('RasterScanType')
