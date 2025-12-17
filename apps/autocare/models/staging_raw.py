##################################################
# DEVELOPMENT MODE ACTIVE
##################################################
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Abbreviation(models.Model):
    abbreviation = models.CharField(db_column='Abbreviation', primary_key=True, max_length=3)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=20)  # Field name made lowercase.
    longdescription = models.CharField(db_column='LongDescription', max_length=200)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Abbreviation'


class Aspiration(models.Model):
    aspirationid = models.IntegerField(db_column='AspirationID', primary_key=True)  # Field name made lowercase.
    aspirationname = models.CharField(db_column='AspirationName', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Aspiration'


class Attachment(models.Model):
    attachmentid = models.IntegerField(db_column='AttachmentID', primary_key=True)  # Field name made lowercase.
    attachmenttypeid = models.IntegerField(db_column='AttachmentTypeID')  # Field name made lowercase.
    attachmentfilename = models.CharField(db_column='AttachmentFileName', max_length=50)  # Field name made lowercase.
    attachmenturl = models.CharField(db_column='AttachmentURL', max_length=100)  # Field name made lowercase.
    attachmentdescription = models.CharField(db_column='AttachmentDescription', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Attachment'


class Attachmenttype(models.Model):
    attachmenttypeid = models.IntegerField(db_column='AttachmentTypeID', primary_key=True)  # Field name made lowercase.
    attachmenttypename = models.CharField(db_column='AttachmentTypeName', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AttachmentType'


class Basevehicle(models.Model):
    basevehicleid = models.IntegerField(db_column='BaseVehicleID', primary_key=True)  # Field name made lowercase.
    yearid = models.ForeignKey('Year', models.DO_NOTHING, db_column='YearID')  # Field name made lowercase.
    makeid = models.ForeignKey('Make', models.DO_NOTHING, db_column='MakeID')  # Field name made lowercase.
    modelid = models.ForeignKey('Model', models.DO_NOTHING, db_column='ModelID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BaseVehicle'


class Bedconfig(models.Model):
    bedconfigid = models.IntegerField(db_column='BedConfigID', primary_key=True)  # Field name made lowercase.
    bedlengthid = models.ForeignKey('Bedlength', models.DO_NOTHING, db_column='BedLengthID')  # Field name made lowercase.
    bedtypeid = models.ForeignKey('Bedtype', models.DO_NOTHING, db_column='BedTypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BedConfig'


class Bedlength(models.Model):
    bedlengthid = models.IntegerField(db_column='BedLengthID', primary_key=True)  # Field name made lowercase.
    bedlength = models.CharField(db_column='BedLength', max_length=10)  # Field name made lowercase.
    bedlengthmetric = models.CharField(db_column='BedLengthMetric', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BedLength'


class Bedtype(models.Model):
    bedtypeid = models.IntegerField(db_column='BedTypeID', primary_key=True)  # Field name made lowercase.
    bedtypename = models.CharField(db_column='BedTypeName', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BedType'


class Bodynumdoors(models.Model):
    bodynumdoorsid = models.IntegerField(db_column='BodyNumDoorsID', primary_key=True)  # Field name made lowercase.
    bodynumdoors = models.CharField(db_column='BodyNumDoors', max_length=3)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BodyNumDoors'


class Bodystyleconfig(models.Model):
    bodystyleconfigid = models.IntegerField(db_column='BodyStyleConfigID', primary_key=True)  # Field name made lowercase.
    bodynumdoorsid = models.ForeignKey(Bodynumdoors, models.DO_NOTHING, db_column='BodyNumDoorsID')  # Field name made lowercase.
    bodytypeid = models.ForeignKey('Bodytype', models.DO_NOTHING, db_column='BodyTypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BodyStyleConfig'


class Bodytype(models.Model):
    bodytypeid = models.IntegerField(db_column='BodyTypeID', primary_key=True)  # Field name made lowercase.
    bodytypename = models.CharField(db_column='BodyTypeName', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BodyType'


class Brakeabs(models.Model):
    brakeabsid = models.IntegerField(db_column='BrakeABSID', primary_key=True)  # Field name made lowercase.
    brakeabsname = models.CharField(db_column='BrakeABSName', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BrakeABS'


class Brakeconfig(models.Model):
    brakeconfigid = models.IntegerField(db_column='BrakeConfigID', primary_key=True)  # Field name made lowercase.
    frontbraketypeid = models.ForeignKey('Braketype', models.DO_NOTHING, db_column='FrontBrakeTypeID')  # Field name made lowercase.
    rearbraketypeid = models.ForeignKey('Braketype', models.DO_NOTHING, db_column='RearBrakeTypeID', related_name='brakeconfig_rearbraketypeid_set')  # Field name made lowercase.
    brakesystemid = models.ForeignKey('Brakesystem', models.DO_NOTHING, db_column='BrakeSystemID')  # Field name made lowercase.
    brakeabsid = models.ForeignKey(Brakeabs, models.DO_NOTHING, db_column='BrakeABSID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BrakeConfig'


class Brakesystem(models.Model):
    brakesystemid = models.IntegerField(db_column='BrakeSystemID', primary_key=True)  # Field name made lowercase.
    brakesystemname = models.CharField(db_column='BrakeSystemName', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BrakeSystem'


class Braketype(models.Model):
    braketypeid = models.IntegerField(db_column='BrakeTypeID', primary_key=True)  # Field name made lowercase.
    braketypename = models.CharField(db_column='BrakeTypeName', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BrakeType'


class Changeattributestates(models.Model):
    changeattributestateid = models.IntegerField(db_column='ChangeAttributeStateID', primary_key=True)  # Field name made lowercase.
    changeattributestate = models.CharField(db_column='ChangeAttributeState', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ChangeAttributeStates'


class Changedetails(models.Model):
    changedetailid = models.IntegerField(db_column='ChangeDetailID', primary_key=True)  # Field name made lowercase.
    changeid = models.ForeignKey('Changes', models.DO_NOTHING, db_column='ChangeID')  # Field name made lowercase.
    changeattributestateid = models.ForeignKey(Changeattributestates, models.DO_NOTHING, db_column='ChangeAttributeStateID')  # Field name made lowercase.
    tablenameid = models.ForeignKey('Changetablenames', models.DO_NOTHING, db_column='TableNameID')  # Field name made lowercase.
    primarykeycolumnname = models.CharField(db_column='PrimaryKeyColumnName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    primarykeybefore = models.IntegerField(db_column='PrimaryKeyBefore', blank=True, null=True)  # Field name made lowercase.
    primarykeyafter = models.IntegerField(db_column='PrimaryKeyAfter', blank=True, null=True)  # Field name made lowercase.
    columnname = models.CharField(db_column='ColumnName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    columnvaluebefore = models.CharField(db_column='ColumnValueBefore', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    columnvalueafter = models.CharField(db_column='ColumnValueAfter', max_length=1000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ChangeDetails'


class Changereasons(models.Model):
    changereasonid = models.IntegerField(db_column='ChangeReasonID', primary_key=True)  # Field name made lowercase.
    changereason = models.CharField(db_column='ChangeReason', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ChangeReasons'


class Changetablenames(models.Model):
    tablenameid = models.IntegerField(db_column='TableNameID', primary_key=True)  # Field name made lowercase.
    tablename = models.CharField(db_column='TableName', max_length=255)  # Field name made lowercase.
    tabledescription = models.CharField(db_column='TableDescription', max_length=1000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ChangeTableNames'


class Changes(models.Model):
    changeid = models.IntegerField(db_column='ChangeID', primary_key=True)  # Field name made lowercase.
    requestid = models.IntegerField(db_column='RequestID')  # Field name made lowercase.
    changereasonid = models.ForeignKey(Changereasons, models.DO_NOTHING, db_column='ChangeReasonID')  # Field name made lowercase.
    revdate = models.DateTimeField(db_column='RevDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Changes'


class Class(models.Model):
    classid = models.IntegerField(db_column='ClassID', primary_key=True)  # Field name made lowercase.
    classname = models.CharField(db_column='ClassName', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Class'


class Cylinderheadtype(models.Model):
    cylinderheadtypeid = models.IntegerField(db_column='CylinderHeadTypeID', primary_key=True)  # Field name made lowercase.
    cylinderheadtypename = models.CharField(db_column='CylinderHeadTypeName', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CylinderHeadType'


class Drivetype(models.Model):
    drivetypeid = models.IntegerField(db_column='DriveTypeID', primary_key=True)  # Field name made lowercase.
    drivetypename = models.CharField(db_column='DriveTypeName', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DriveType'


class Eleccontrolled(models.Model):
    eleccontrolledid = models.IntegerField(db_column='ElecControlledID', primary_key=True)  # Field name made lowercase.
    eleccontrolled = models.CharField(db_column='ElecControlled', max_length=3)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ElecControlled'


class Enginebase(models.Model):
    enginebaseid = models.IntegerField(db_column='EngineBaseID', primary_key=True)  # Field name made lowercase.
    liter = models.CharField(db_column='Liter', max_length=6)  # Field name made lowercase.
    cc = models.CharField(db_column='CC', max_length=8)  # Field name made lowercase.
    cid = models.CharField(db_column='CID', max_length=7)  # Field name made lowercase.
    cylinders = models.CharField(db_column='Cylinders', max_length=2)  # Field name made lowercase.
    blocktype = models.CharField(db_column='BlockType', max_length=2)  # Field name made lowercase.
    engborein = models.CharField(db_column='EngBoreIn', max_length=10)  # Field name made lowercase.
    engboremetric = models.CharField(db_column='EngBoreMetric', max_length=10)  # Field name made lowercase.
    engstrokein = models.CharField(db_column='EngStrokeIn', max_length=10)  # Field name made lowercase.
    engstrokemetric = models.CharField(db_column='EngStrokeMetric', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EngineBase'


class Enginebase2(models.Model):
    enginebaseid = models.IntegerField(db_column='EngineBaseID', primary_key=True)  # Field name made lowercase.
    engineblockid = models.ForeignKey('Engineblock', models.DO_NOTHING, db_column='EngineBlockID')  # Field name made lowercase.
    engineborestrokeid = models.ForeignKey('Engineborestroke', models.DO_NOTHING, db_column='EngineBoreStrokeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EngineBase2'


class Engineblock(models.Model):
    engineblockid = models.IntegerField(db_column='EngineBlockID', primary_key=True)  # Field name made lowercase.
    liter = models.CharField(db_column='Liter', max_length=6)  # Field name made lowercase.
    cc = models.CharField(db_column='CC', max_length=8)  # Field name made lowercase.
    cid = models.CharField(db_column='CID', max_length=7)  # Field name made lowercase.
    cylinders = models.CharField(db_column='Cylinders', max_length=2)  # Field name made lowercase.
    blocktype = models.CharField(db_column='BlockType', max_length=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EngineBlock'


class Engineborestroke(models.Model):
    engineborestrokeid = models.IntegerField(db_column='EngineBoreStrokeID', primary_key=True)  # Field name made lowercase.
    engborein = models.CharField(db_column='EngBoreIn', max_length=10)  # Field name made lowercase.
    engboremetric = models.CharField(db_column='EngBoreMetric', max_length=10)  # Field name made lowercase.
    engstrokein = models.CharField(db_column='EngStrokeIn', max_length=10)  # Field name made lowercase.
    engstrokemetric = models.CharField(db_column='EngStrokeMetric', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EngineBoreStroke'


class Engineconfig(models.Model):
    engineconfigid = models.IntegerField(db_column='EngineConfigID', primary_key=True)  # Field name made lowercase.
    enginedesignationid = models.ForeignKey('Enginedesignation', models.DO_NOTHING, db_column='EngineDesignationID')  # Field name made lowercase.
    enginevinid = models.ForeignKey('Enginevin', models.DO_NOTHING, db_column='EngineVINID')  # Field name made lowercase.
    valvesid = models.ForeignKey('Valves', models.DO_NOTHING, db_column='ValvesID')  # Field name made lowercase.
    enginebaseid = models.ForeignKey(Enginebase, models.DO_NOTHING, db_column='EngineBaseID')  # Field name made lowercase.
    fueldeliveryconfigid = models.ForeignKey('Fueldeliveryconfig', models.DO_NOTHING, db_column='FuelDeliveryConfigID')  # Field name made lowercase.
    aspirationid = models.ForeignKey(Aspiration, models.DO_NOTHING, db_column='AspirationID')  # Field name made lowercase.
    cylinderheadtypeid = models.ForeignKey(Cylinderheadtype, models.DO_NOTHING, db_column='CylinderHeadTypeID')  # Field name made lowercase.
    fueltypeid = models.ForeignKey('Fueltype', models.DO_NOTHING, db_column='FuelTypeID')  # Field name made lowercase.
    ignitionsystemtypeid = models.ForeignKey('Ignitionsystemtype', models.DO_NOTHING, db_column='IgnitionSystemTypeID')  # Field name made lowercase.
    enginemfrid = models.ForeignKey('Mfr', models.DO_NOTHING, db_column='EngineMfrID')  # Field name made lowercase.
    engineversionid = models.ForeignKey('Engineversion', models.DO_NOTHING, db_column='EngineVersionID')  # Field name made lowercase.
    poweroutputid = models.IntegerField(db_column='PowerOutputID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EngineConfig'


class Engineconfig2(models.Model):
    engineconfigid = models.IntegerField(db_column='EngineConfigID', primary_key=True)  # Field name made lowercase.
    enginedesignationid = models.ForeignKey('Enginedesignation', models.DO_NOTHING, db_column='EngineDesignationID')  # Field name made lowercase.
    enginevinid = models.ForeignKey('Enginevin', models.DO_NOTHING, db_column='EngineVINID')  # Field name made lowercase.
    valvesid = models.ForeignKey('Valves', models.DO_NOTHING, db_column='ValvesID')  # Field name made lowercase.
    enginebaseid = models.ForeignKey(Enginebase2, models.DO_NOTHING, db_column='EngineBaseID')  # Field name made lowercase.
    engineblockid = models.ForeignKey(Engineblock, models.DO_NOTHING, db_column='EngineBlockID')  # Field name made lowercase.
    engineborestrokeid = models.ForeignKey(Engineborestroke, models.DO_NOTHING, db_column='EngineBoreStrokeID')  # Field name made lowercase.
    fueldeliveryconfigid = models.ForeignKey('Fueldeliveryconfig', models.DO_NOTHING, db_column='FuelDeliveryConfigID')  # Field name made lowercase.
    aspirationid = models.ForeignKey(Aspiration, models.DO_NOTHING, db_column='AspirationID')  # Field name made lowercase.
    cylinderheadtypeid = models.ForeignKey(Cylinderheadtype, models.DO_NOTHING, db_column='CylinderHeadTypeID')  # Field name made lowercase.
    fueltypeid = models.ForeignKey('Fueltype', models.DO_NOTHING, db_column='FuelTypeID')  # Field name made lowercase.
    ignitionsystemtypeid = models.ForeignKey('Ignitionsystemtype', models.DO_NOTHING, db_column='IgnitionSystemTypeID')  # Field name made lowercase.
    enginemfrid = models.ForeignKey('Mfr', models.DO_NOTHING, db_column='EngineMfrID')  # Field name made lowercase.
    engineversionid = models.ForeignKey('Engineversion', models.DO_NOTHING, db_column='EngineVersionID')  # Field name made lowercase.
    poweroutputid = models.IntegerField(db_column='PowerOutputID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EngineConfig2'


class Enginedesignation(models.Model):
    enginedesignationid = models.IntegerField(db_column='EngineDesignationID', primary_key=True)  # Field name made lowercase.
    enginedesignationname = models.CharField(db_column='EngineDesignationName', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EngineDesignation'


class Enginevin(models.Model):
    enginevinid = models.IntegerField(db_column='EngineVINID', primary_key=True)  # Field name made lowercase.
    enginevinname = models.CharField(db_column='EngineVINName', max_length=5)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EngineVIN'


class Engineversion(models.Model):
    engineversionid = models.IntegerField(db_column='EngineVersionID', primary_key=True)  # Field name made lowercase.
    engineversion = models.CharField(db_column='EngineVersion', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EngineVersion'


class Englishphrase(models.Model):
    englishphraseid = models.IntegerField(db_column='EnglishPhraseID', primary_key=True)  # Field name made lowercase.
    englishphrase = models.CharField(db_column='EnglishPhrase', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EnglishPhrase'


class Fueldeliveryconfig(models.Model):
    fueldeliveryconfigid = models.IntegerField(db_column='FuelDeliveryConfigID', primary_key=True)  # Field name made lowercase.
    fueldeliverytypeid = models.ForeignKey('Fueldeliverytype', models.DO_NOTHING, db_column='FuelDeliveryTypeID')  # Field name made lowercase.
    fueldeliverysubtypeid = models.ForeignKey('Fueldeliverysubtype', models.DO_NOTHING, db_column='FuelDeliverySubTypeID')  # Field name made lowercase.
    fuelsystemcontroltypeid = models.ForeignKey('Fuelsystemcontroltype', models.DO_NOTHING, db_column='FuelSystemControlTypeID')  # Field name made lowercase.
    fuelsystemdesignid = models.ForeignKey('Fuelsystemdesign', models.DO_NOTHING, db_column='FuelSystemDesignID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FuelDeliveryConfig'


class Fueldeliverysubtype(models.Model):
    fueldeliverysubtypeid = models.IntegerField(db_column='FuelDeliverySubTypeID', primary_key=True)  # Field name made lowercase.
    fueldeliverysubtypename = models.CharField(db_column='FuelDeliverySubTypeName', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FuelDeliverySubType'


class Fueldeliverytype(models.Model):
    fueldeliverytypeid = models.IntegerField(db_column='FuelDeliveryTypeID', primary_key=True)  # Field name made lowercase.
    fueldeliverytypename = models.CharField(db_column='FuelDeliveryTypeName', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FuelDeliveryType'


class Fuelsystemcontroltype(models.Model):
    fuelsystemcontroltypeid = models.IntegerField(db_column='FuelSystemControlTypeID', primary_key=True)  # Field name made lowercase.
    fuelsystemcontroltypename = models.CharField(db_column='FuelSystemControlTypeName', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FuelSystemControlType'


class Fuelsystemdesign(models.Model):
    fuelsystemdesignid = models.IntegerField(db_column='FuelSystemDesignID', primary_key=True)  # Field name made lowercase.
    fuelsystemdesignname = models.CharField(db_column='FuelSystemDesignName', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FuelSystemDesign'


class Fueltype(models.Model):
    fueltypeid = models.IntegerField(db_column='FuelTypeID', primary_key=True)  # Field name made lowercase.
    fueltypename = models.CharField(db_column='FuelTypeName', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FuelType'


class Ignitionsystemtype(models.Model):
    ignitionsystemtypeid = models.IntegerField(db_column='IgnitionSystemTypeID', primary_key=True)  # Field name made lowercase.
    ignitionsystemtypename = models.CharField(db_column='IgnitionSystemTypeName', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'IgnitionSystemType'


class Language(models.Model):
    languageid = models.IntegerField(db_column='LanguageID', primary_key=True)  # Field name made lowercase.
    languagename = models.CharField(db_column='LanguageName', max_length=20)  # Field name made lowercase.
    dialectname = models.CharField(db_column='DialectName', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Language'


class Languagetranslation(models.Model):
    languagetranslationid = models.IntegerField(db_column='LanguageTranslationID', primary_key=True)  # Field name made lowercase.
    englishphraseid = models.IntegerField(db_column='EnglishPhraseID')  # Field name made lowercase.
    languageid = models.IntegerField(db_column='LanguageID')  # Field name made lowercase.
    translation = models.CharField(db_column='Translation', max_length=150)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LanguageTranslation'


class Languagetranslationattachment(models.Model):
    languagetranslationattachmentid = models.IntegerField(db_column='LanguageTranslationAttachmentID', primary_key=True)  # Field name made lowercase.
    languagetranslationid = models.IntegerField(db_column='LanguageTranslationID')  # Field name made lowercase.
    attachmentid = models.IntegerField(db_column='AttachmentID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LanguageTranslationAttachment'


class Make(models.Model):
    makeid = models.IntegerField(db_column='MakeID', primary_key=True)  # Field name made lowercase.
    makename = models.CharField(db_column='MakeName', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Make'


class Mfr(models.Model):
    mfrid = models.IntegerField(db_column='MfrID', primary_key=True)  # Field name made lowercase.
    mfrname = models.CharField(db_column='MfrName', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mfr'


class Mfrbodycode(models.Model):
    mfrbodycodeid = models.IntegerField(db_column='MfrBodyCodeID', primary_key=True)  # Field name made lowercase.
    mfrbodycodename = models.CharField(db_column='MfrBodyCodeName', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MfrBodyCode'


class Model(models.Model):
    modelid = models.IntegerField(db_column='ModelID', primary_key=True)  # Field name made lowercase.
    modelname = models.CharField(db_column='ModelName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    vehicletypeid = models.ForeignKey('Vehicletype', models.DO_NOTHING, db_column='VehicleTypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Model'


class Poweroutput(models.Model):
    poweroutputid = models.IntegerField(db_column='PowerOutputID')  # Field name made lowercase.
    horsepower = models.CharField(db_column='HorsePower', max_length=10)  # Field name made lowercase.
    kilowattpower = models.CharField(db_column='KilowattPower', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PowerOutput'


class Publicationstage(models.Model):
    publicationstageid = models.IntegerField(db_column='PublicationStageID', primary_key=True)  # Field name made lowercase.
    publicationstagename = models.CharField(db_column='PublicationStageName', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PublicationStage'


class Region(models.Model):
    regionid = models.IntegerField(db_column='RegionID', primary_key=True)  # Field name made lowercase.
    parentid = models.ForeignKey('self', models.DO_NOTHING, db_column='ParentID', blank=True, null=True)  # Field name made lowercase.
    regionabbr = models.CharField(db_column='RegionAbbr', max_length=3, blank=True, null=True)  # Field name made lowercase.
    regionname = models.CharField(db_column='RegionName', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Region'


class Springtype(models.Model):
    springtypeid = models.IntegerField(db_column='SpringTypeID', primary_key=True)  # Field name made lowercase.
    springtypename = models.CharField(db_column='SpringTypeName', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SpringType'


class Springtypeconfig(models.Model):
    springtypeconfigid = models.IntegerField(db_column='SpringTypeConfigID', primary_key=True)  # Field name made lowercase.
    frontspringtypeid = models.ForeignKey(Springtype, models.DO_NOTHING, db_column='FrontSpringTypeID')  # Field name made lowercase.
    rearspringtypeid = models.ForeignKey(Springtype, models.DO_NOTHING, db_column='RearSpringTypeID', related_name='springtypeconfig_rearspringtypeid_set')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SpringTypeConfig'


class Steeringconfig(models.Model):
    steeringconfigid = models.IntegerField(db_column='SteeringConfigID', primary_key=True)  # Field name made lowercase.
    steeringtypeid = models.ForeignKey('Steeringtype', models.DO_NOTHING, db_column='SteeringTypeID')  # Field name made lowercase.
    steeringsystemid = models.ForeignKey('Steeringsystem', models.DO_NOTHING, db_column='SteeringSystemID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SteeringConfig'


class Steeringsystem(models.Model):
    steeringsystemid = models.IntegerField(db_column='SteeringSystemID', primary_key=True)  # Field name made lowercase.
    steeringsystemname = models.CharField(db_column='SteeringSystemName', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SteeringSystem'


class Steeringtype(models.Model):
    steeringtypeid = models.IntegerField(db_column='SteeringTypeID', primary_key=True)  # Field name made lowercase.
    steeringtypename = models.CharField(db_column='SteeringTypeName', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SteeringType'


class Submodel(models.Model):
    submodelid = models.IntegerField(db_column='SubmodelID', primary_key=True)  # Field name made lowercase.
    submodelname = models.CharField(db_column='SubModelName', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SubModel'


class Transmission(models.Model):
    transmissionid = models.IntegerField(db_column='TransmissionID', primary_key=True)  # Field name made lowercase.
    transmissionbaseid = models.ForeignKey('Transmissionbase', models.DO_NOTHING, db_column='TransmissionBaseID')  # Field name made lowercase.
    transmissionmfrcodeid = models.ForeignKey('Transmissionmfrcode', models.DO_NOTHING, db_column='TransmissionMfrCodeID')  # Field name made lowercase.
    transmissioneleccontrolledid = models.ForeignKey(Eleccontrolled, models.DO_NOTHING, db_column='TransmissionElecControlledID')  # Field name made lowercase.
    transmissionmfrid = models.ForeignKey(Mfr, models.DO_NOTHING, db_column='TransmissionMfrID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Transmission'


class Transmissionbase(models.Model):
    transmissionbaseid = models.IntegerField(db_column='TransmissionBaseID', primary_key=True)  # Field name made lowercase.
    transmissiontypeid = models.ForeignKey('Transmissiontype', models.DO_NOTHING, db_column='TransmissionTypeID')  # Field name made lowercase.
    transmissionnumspeedsid = models.ForeignKey('Transmissionnumspeeds', models.DO_NOTHING, db_column='TransmissionNumSpeedsID')  # Field name made lowercase.
    transmissioncontroltypeid = models.ForeignKey('Transmissioncontroltype', models.DO_NOTHING, db_column='TransmissionControlTypeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TransmissionBase'


class Transmissioncontroltype(models.Model):
    transmissioncontroltypeid = models.IntegerField(db_column='TransmissionControlTypeID', primary_key=True)  # Field name made lowercase.
    transmissioncontroltypename = models.CharField(db_column='TransmissionControlTypeName', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TransmissionControlType'


class Transmissionmfrcode(models.Model):
    transmissionmfrcodeid = models.IntegerField(db_column='TransmissionMfrCodeID', primary_key=True)  # Field name made lowercase.
    transmissionmfrcode = models.CharField(db_column='TransmissionMfrCode', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TransmissionMfrCode'


class Transmissionnumspeeds(models.Model):
    transmissionnumspeedsid = models.IntegerField(db_column='TransmissionNumSpeedsID', primary_key=True)  # Field name made lowercase.
    transmissionnumspeeds = models.CharField(db_column='TransmissionNumSpeeds', max_length=3)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TransmissionNumSpeeds'


class Transmissiontype(models.Model):
    transmissiontypeid = models.IntegerField(db_column='TransmissionTypeID', primary_key=True)  # Field name made lowercase.
    transmissiontypename = models.CharField(db_column='TransmissionTypeName', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TransmissionType'


class Vcdbchanges(models.Model):
    versiondate = models.DateTimeField(db_column='VersionDate')  # Field name made lowercase.
    tablename = models.CharField(db_column='TableName', max_length=30)  # Field name made lowercase.
    id = models.IntegerField(db_column='ID')  # Field name made lowercase.
    action = models.CharField(db_column='Action', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VCdbChanges'


class Valves(models.Model):
    valvesid = models.IntegerField(db_column='ValvesID', primary_key=True)  # Field name made lowercase.
    valvesperengine = models.CharField(db_column='ValvesPerEngine', max_length=3)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Valves'


class Vehicle(models.Model):
    vehicleid = models.IntegerField(db_column='VehicleID', primary_key=True)  # Field name made lowercase.
    basevehicleid = models.ForeignKey(Basevehicle, models.DO_NOTHING, db_column='BaseVehicleID')  # Field name made lowercase.
    submodelid = models.ForeignKey(Submodel, models.DO_NOTHING, db_column='SubmodelID')  # Field name made lowercase.
    regionid = models.ForeignKey(Region, models.DO_NOTHING, db_column='RegionID')  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=10, blank=True, null=True)  # Field name made lowercase.
    publicationstageid = models.ForeignKey(Publicationstage, models.DO_NOTHING, db_column='PublicationStageID')  # Field name made lowercase.
    publicationstagesource = models.CharField(db_column='PublicationStageSource', max_length=100)  # Field name made lowercase.
    publicationstagedate = models.DateTimeField(db_column='PublicationStageDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Vehicle'


class Vehicletobedconfig(models.Model):
    vehicletobedconfigid = models.IntegerField(db_column='VehicleToBedConfigID', primary_key=True)  # Field name made lowercase.
    vehicleid = models.ForeignKey(Vehicle, models.DO_NOTHING, db_column='VehicleID')  # Field name made lowercase.
    bedconfigid = models.ForeignKey(Bedconfig, models.DO_NOTHING, db_column='BedConfigID')  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VehicleToBedConfig'


class Vehicletobodyconfig(models.Model):
    vehicletobodyconfigid = models.IntegerField(db_column='VehicleToBodyConfigID', primary_key=True)  # Field name made lowercase.
    vehicleid = models.ForeignKey(Vehicle, models.DO_NOTHING, db_column='VehicleID')  # Field name made lowercase.
    wheelbaseid = models.ForeignKey('Wheelbase', models.DO_NOTHING, db_column='WheelBaseID')  # Field name made lowercase.
    bedconfigid = models.ForeignKey(Bedconfig, models.DO_NOTHING, db_column='BedConfigID')  # Field name made lowercase.
    bodystyleconfigid = models.ForeignKey(Bodystyleconfig, models.DO_NOTHING, db_column='BodyStyleConfigID')  # Field name made lowercase.
    mfrbodycodeid = models.ForeignKey(Mfrbodycode, models.DO_NOTHING, db_column='MfrBodyCodeID')  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VehicleToBodyConfig'


class Vehicletobodystyleconfig(models.Model):
    vehicletobodystyleconfigid = models.IntegerField(db_column='VehicleToBodyStyleConfigID', primary_key=True)  # Field name made lowercase.
    vehicleid = models.ForeignKey(Vehicle, models.DO_NOTHING, db_column='VehicleID')  # Field name made lowercase.
    bodystyleconfigid = models.ForeignKey(Bodystyleconfig, models.DO_NOTHING, db_column='BodyStyleConfigID')  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VehicleToBodyStyleConfig'


class Vehicletobrakeconfig(models.Model):
    vehicletobrakeconfigid = models.IntegerField(db_column='VehicleToBrakeConfigID', primary_key=True)  # Field name made lowercase.
    vehicleid = models.ForeignKey(Vehicle, models.DO_NOTHING, db_column='VehicleID')  # Field name made lowercase.
    brakeconfigid = models.ForeignKey(Brakeconfig, models.DO_NOTHING, db_column='BrakeConfigID')  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VehicleToBrakeConfig'


class Vehicletoclass(models.Model):
    vehicletoclassid = models.IntegerField(db_column='VehicleToClassID', primary_key=True)  # Field name made lowercase.
    vehicleid = models.ForeignKey(Vehicle, models.DO_NOTHING, db_column='VehicleID')  # Field name made lowercase.
    classid = models.ForeignKey(Class, models.DO_NOTHING, db_column='ClassID')  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VehicleToClass'


class Vehicletodrivetype(models.Model):
    vehicletodrivetypeid = models.IntegerField(db_column='VehicleToDriveTypeID', primary_key=True)  # Field name made lowercase.
    vehicleid = models.ForeignKey(Vehicle, models.DO_NOTHING, db_column='VehicleID')  # Field name made lowercase.
    drivetypeid = models.ForeignKey(Drivetype, models.DO_NOTHING, db_column='DriveTypeID')  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VehicleToDriveType'


class Vehicletoengineconfig(models.Model):
    vehicletoengineconfigid = models.IntegerField(db_column='VehicleToEngineConfigID', primary_key=True)  # Field name made lowercase.
    vehicleid = models.ForeignKey(Vehicle, models.DO_NOTHING, db_column='VehicleID')  # Field name made lowercase.
    engineconfigid = models.ForeignKey(Engineconfig2, models.DO_NOTHING, db_column='EngineConfigID')  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VehicleToEngineConfig'


class Vehicletomfrbodycode(models.Model):
    vehicletomfrbodycodeid = models.IntegerField(db_column='VehicleToMfrBodyCodeID', primary_key=True)  # Field name made lowercase.
    vehicleid = models.ForeignKey(Vehicle, models.DO_NOTHING, db_column='VehicleID')  # Field name made lowercase.
    mfrbodycodeid = models.ForeignKey(Mfrbodycode, models.DO_NOTHING, db_column='MfrBodyCodeID')  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VehicleToMfrBodyCode'


class Vehicletospringtypeconfig(models.Model):
    vehicletospringtypeconfigid = models.IntegerField(db_column='VehicleToSpringTypeConfigID', primary_key=True)  # Field name made lowercase.
    vehicleid = models.ForeignKey(Vehicle, models.DO_NOTHING, db_column='VehicleID')  # Field name made lowercase.
    springtypeconfigid = models.ForeignKey(Springtypeconfig, models.DO_NOTHING, db_column='SpringTypeConfigID')  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VehicleToSpringTypeConfig'


class Vehicletosteeringconfig(models.Model):
    vehicletosteeringconfigid = models.IntegerField(db_column='VehicleToSteeringConfigID', primary_key=True)  # Field name made lowercase.
    vehicleid = models.ForeignKey(Vehicle, models.DO_NOTHING, db_column='VehicleID')  # Field name made lowercase.
    steeringconfigid = models.ForeignKey(Steeringconfig, models.DO_NOTHING, db_column='SteeringConfigID')  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VehicleToSteeringConfig'


class Vehicletotransmission(models.Model):
    vehicletotransmissionid = models.IntegerField(db_column='VehicleToTransmissionID', primary_key=True)  # Field name made lowercase.
    vehicleid = models.ForeignKey(Vehicle, models.DO_NOTHING, db_column='VehicleID')  # Field name made lowercase.
    transmissionid = models.ForeignKey(Transmission, models.DO_NOTHING, db_column='TransmissionID')  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VehicleToTransmission'


class Vehicletowheelbase(models.Model):
    vehicletowheelbaseid = models.IntegerField(db_column='VehicleToWheelBaseID', primary_key=True)  # Field name made lowercase.
    vehicleid = models.ForeignKey(Vehicle, models.DO_NOTHING, db_column='VehicleID')  # Field name made lowercase.
    wheelbaseid = models.IntegerField(db_column='WheelBaseID')  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VehicleToWheelBase'


class Vehicletype(models.Model):
    vehicletypeid = models.IntegerField(db_column='VehicleTypeID', primary_key=True)  # Field name made lowercase.
    vehicletypename = models.CharField(db_column='VehicleTypeName', max_length=50)  # Field name made lowercase.
    vehicletypegroupid = models.IntegerField(db_column='VehicleTypeGroupID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VehicleType'


class Vehicletypegroup(models.Model):
    vehicletypegroupid = models.IntegerField(db_column='VehicleTypeGroupID')  # Field name made lowercase.
    vehicletypegroupname = models.CharField(db_column='VehicleTypeGroupName', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VehicleTypeGroup'


class Version(models.Model):
    versiondate = models.DateField(db_column='VersionDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Version'


class Wheelbase(models.Model):
    wheelbaseid = models.IntegerField(db_column='WheelBaseID', primary_key=True)  # Field name made lowercase.
    wheelbase = models.CharField(db_column='WheelBase', max_length=10)  # Field name made lowercase.
    wheelbasemetric = models.CharField(db_column='WheelBaseMetric', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WheelBase'


class Year(models.Model):
    yearid = models.IntegerField(db_column='YearID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Year'
