from __future__ import unicode_literals

from builtins import str

from django.db import models
from django.db.models import Prefetch
from geo.models import Location
from docs.models import Doc
#from django.utils.translation import gettext_lazy as _


class NamedModelAbstractBase(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return str(self.id) + ", " + self.name

    class Meta:
        abstract = True

class AfricanInfo(NamedModelAbstractBase):
    """
    Used to capture information about the ethnicity or background of the
    captives on a ship if found in merchants records or newspaper ads
    """
    pass
    possibly_offensive = models.BooleanField(
        default=False,
        help_text="Indicates that the wording used in this label might be offensive to readers")




class CargoType(NamedModelAbstractBase):
    """
    Types of cargo that were shipped on the voyage along with captives.
    """
    pass
    
class CargoUnit(NamedModelAbstractBase):
    """
    A unit of measure associated with cargo (weight/volume etc).
    """
    pass


# Voyage Regions and Places
class BroadRegion(models.Model):
	"""
	Broad Regions (continents).
	"""
	
	geo_location = models.ForeignKey(Location,
									on_delete=models.CASCADE,
									verbose_name="Location",
									null=True)

	def __str__(self):
		return self.geo_location.name

	class Meta:
		verbose_name = "Broad region (area)"
		verbose_name_plural = "Broad regions (areas)"


class Region(models.Model):
	"""
	Specific Regions (countries or colonies).
	related to: :class:`~voyages.apps.voyage.models.BroadRegion`
	"""

	geo_location = models.ForeignKey(Location,
									on_delete=models.CASCADE,
									verbose_name="Location",
									null=True)

	class Meta:
		verbose_name = "Region"
		verbose_name_plural = "Regions"

	def __str__(self):
		return self.geo_location.name


class Place(models.Model):
	"""
	Place (port or location).
	related to: :class:`voyages.apps.voyage.modles.Region`
	"""
	
	geo_location = models.ForeignKey(Location,
									on_delete=models.CASCADE,
									verbose_name="Location",
									null=True)
	
	class Meta:
		verbose_name = "Place (Port or Location)"
		verbose_name_plural = "Places (Ports or Locations)"

	def __str__(self):
		return self.geo_location.name


# Voyage Groupings
# check for mismatch in VoyageGroupings class
class VoyageGroupings(models.Model):
	"""
	Labels for groupings names.
	"""
	name = models.CharField(max_length=30)
	value = models.IntegerField()
	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Grouping for estimating imputed slaves"
		verbose_name_plural = "Groupings for estimating imputed slaves"


# Voyage Ship, Nation, Owners
class Nationality(models.Model):
	"""
	Nationality of ships.
	"""
	name = models.CharField(max_length=255)
	value = models.IntegerField()
	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Nationality"
		verbose_name_plural = "Nationalities"
		ordering = ['value']

class TonType(models.Model):
	"""
	Types of tonnage.
	"""
	name = models.CharField(max_length=255)
	value = models.IntegerField()
	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Type of tons"
		verbose_name_plural = "Types of tons"
		ordering = ['value']


class RigOfVessel(models.Model):
	"""
	Rig of Vessel.
	"""
	name = models.CharField(max_length=25)
	value = models.IntegerField()
	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Rig of vessel"
		verbose_name_plural = "Rigs of vessel"
		ordering = ['value']

class VoyageShip(models.Model):
	"""
	Information about voyage ship.
	related to: :class:`~voyages.apps.voyage.models.Region`
	related to: :class:`~voyages.apps.voyage.models.Place`
	related to: :class:`~voyages.apps.voyage.models.Voyage`
	related to: :class:`~voyages.apps.voyage.models.Nationality`
	related to: :class:`~voyages.apps.voyage.models.TonType`
	related to: :class:`~voyages.apps.voyage.models.RigOfVessel`
	"""

	# Data variables
	ship_name = models.CharField("Name of vessel",
								 max_length=255,
								 null=True,
								 blank=True)
	nationality_ship = models.ForeignKey('Nationality',
										 related_name="nationality_ship",
										 null=True,
										 blank=True,
										 on_delete=models.CASCADE,
										 verbose_name="Ship Nationality")
	tonnage = models.IntegerField("Tonnage of vessel", null=True, blank=True)
	ton_type = models.ForeignKey('TonType', null=True, blank=True,
								 on_delete=models.CASCADE, verbose_name="Type of Tonnage")
	rig_of_vessel = models.ForeignKey('RigOfVessel', null=True, blank=True,
									  on_delete=models.CASCADE, verbose_name="Rig of Vessel")
	guns_mounted = models.IntegerField("Guns mounted", null=True, blank=True)
	year_of_construction = models.IntegerField("Year of vessel's construction",
											   null=True,
											   blank=True)
	vessel_construction_place = models.ForeignKey(
		'Place',
		related_name="vessel_construction_place",
		verbose_name="Place where vessel constructed",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	vessel_construction_region = models.ForeignKey(
		'Region',
		related_name="vessel_construction_region",
		verbose_name="Region where vessel constructed",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	registered_year = models.IntegerField("Year of vessel's registration",
										  null=True,
										  blank=True)
	registered_place = models.ForeignKey(
		'Place',
		related_name="registered_place",
		verbose_name="Place where vessel registered",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	registered_region = models.ForeignKey(
		'Region',
		related_name="registered_region",
		verbose_name="Region where vessel registered",
		null=True,
		blank=True,
		on_delete=models.CASCADE)

	# Imputed variables
	imputed_nationality = models.ForeignKey('Nationality',
											related_name="imputed_nationality",
											verbose_name="Imputed Ship Nationality",
											null=True,
											blank=True,
											on_delete=models.CASCADE)
	tonnage_mod = models.DecimalField(
		"Tonnage standardized on British"
		" measured tons 1773-1870",
		max_digits=8,
		decimal_places=1,
		null=True,
		blank=True)

	voyage = models.ForeignKey('Voyage',
							   null=True,
							   blank=True,
							   on_delete=models.CASCADE)

	def __str__(self):
		return self.ship_name if self.ship_name is not None else "None"

	class Meta:
		verbose_name = "Ship"
		verbose_name_plural = "Ships"


class VoyageShipOwner(models.Model):
	"""
	Owner name.
	Represents first_owner, second_owner, ...
	"""
	name = models.CharField(max_length=255)
	class Meta:
		verbose_name = "Ship Owner"
		verbose_name_plural = "Ship Owners"
	def __str__(self):
		return self.name


class VoyageShipOwnerConnection(models.Model):
	"""
	Represents the relation between Voyage Ship owners and
	Owner.
	owner_order represents order of each owner (1st, 2nd, ...)
	"""
	owner = models.ForeignKey(	'VoyageShipOwner',
								verbose_name="Ship Owner",
							  	on_delete=models.CASCADE)
	voyage = models.ForeignKey(	'Voyage',
							  	 on_delete=models.CASCADE,
							   	related_name='voyage_shipownerconnection')
	owner_order = models.IntegerField()

	def __str__(self):
		return "Ship owner:"


class VoyageCargoConnection(models.Model):
    """
    Specifies cargo that was shipped together with captives.
    """
    cargo = models.ForeignKey(CargoType, related_name="+",
                              on_delete=models.CASCADE)
    voyage = models.ForeignKey('Voyage', related_name="+",
                               on_delete=models.CASCADE)
    unit = models.ForeignKey(CargoUnit, related_name="+", null=True,on_delete=models.CASCADE)
    amount = models.FloatField("The amount of cargo according to the unit", null=True)

    class Meta:
        unique_together = ['voyage', 'cargo']

# Voyage Outcome
class ParticularOutcome(models.Model):
	"""
	Particular outcome.
	"""
	name = models.CharField("Outcome label", max_length=200)
	value = models.IntegerField("Code of outcome")
	def __str__(self):
		return self.name
	class Meta:
		ordering = ['value']
		verbose_name = "Fate (particular outcome of voyage)"
		verbose_name_plural = "Fates (particular outcomes of voyages)"


class SlavesOutcome(models.Model):
	"""
	Outcome of voyage for slaves.
	"""
	name = models.CharField("Outcome label", max_length=200)
	value = models.IntegerField("Code of outcome")
	def __str__(self):
		return self.name
	class Meta:
		verbose_name = "Captives Outcome"
		verbose_name_plural = "Captives' Outcomes"
		ordering = ['value']


class VesselCapturedOutcome(models.Model):
	"""
	Outcome of voyage if vessel captured.
	"""
	name = models.CharField("Outcome label", max_length=200)
	value = models.IntegerField("Code of outcome")
	def __str__(self):
		return self.name
	class Meta:
		verbose_name = "Vessel Captured Outcome"
		verbose_name_plural = "Vessel Captured Outcomes"
		ordering = ['value']


class OwnerOutcome(models.Model):
	"""
	Outcome of voyage for owner.
	"""
	name = models.CharField("Outcome label", max_length=200)
	value = models.IntegerField("Code of outcome")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name='Owner Outcome'
		verbose_name_plural='Owner Outcomes'
		ordering = ['value']


class Resistance(models.Model):
	"""
	Resistance labels
	"""
	name = models.CharField("Resistance label", max_length=255)
	value = models.IntegerField("Code of resistance")
	def __str__(self):
		return self.name
	class Meta:
		verbose_name='Resistance'
		verbose_name_plural='Resistances'
		ordering = ['value']


class VoyageOutcome(models.Model):
	"""
	Information about Outcomes
	"""

	# Data variables
	particular_outcome = models.ForeignKey('ParticularOutcome',
										   verbose_name="Particular Outcome",
										   null=True,
										   blank=True,
										   on_delete=models.CASCADE)
	resistance = models.ForeignKey('Resistance',
								   verbose_name="Resistance",
								   null=True,
								   blank=True,
								   on_delete=models.CASCADE)

	# Imputed variables
	outcome_slaves = models.ForeignKey('SlavesOutcome',
									   verbose_name="Slaves Outcome",
									   null=True,
									   blank=True,
									   on_delete=models.CASCADE)
	vessel_captured_outcome = models.ForeignKey(
		'VesselCapturedOutcome',
		verbose_name="Vessel Captured Outcome",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	outcome_owner = models.ForeignKey('OwnerOutcome',
									  verbose_name="Owner Outcome",
									  null=True,
									  blank=True,
									  on_delete=models.CASCADE)

	voyage = models.ForeignKey('Voyage',
							   null=True,
							   blank=True,
							   on_delete=models.CASCADE)
	
	def __str__(self):
		# TODO: We may want to change this.
		#return "Outcome"
		return '%s %s %s %s' %(
				self.particular_outcome,
				self.resistance,
				self.outcome_slaves,
				self.vessel_captured_outcome
				)

	class Meta:
		verbose_name = "Outcome"
		verbose_name_plural = "Outcomes"


# Voyage Itinerary
class VoyageItinerary(models.Model):
	"""
	Voyage Itinerary data.
	related to: :class:`~voyages.apps.voyage.models.BroadRegion`
	related to: :class:`~voyages.apps.voyage.models.SpecificRegion`
	related to: :class:`~voyages.apps.voyage.models.Place`
	"""

	# Data variables
	port_of_departure = models.ForeignKey(
		'Place',
		related_name="port_of_departure",
		verbose_name="Port of departure (PORTDEP)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	# Intended variables
	int_first_port_emb = models.ForeignKey(
		'Place',
		related_name="int_first_port_emb",
		verbose_name="First intended port of embarkation (EMBPORT)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	int_second_port_emb = models.ForeignKey(
		'Place',
		related_name="int_second_port_emb",
		verbose_name="Second intended port of embarkation (EMBPORT2)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	int_first_region_purchase_slaves = models.ForeignKey(
		'Region',
		related_name="int_first_region_purchase_slaves",
		verbose_name="First intended region of purchase of slaves (EMBREG)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	int_second_region_purchase_slaves = models.ForeignKey(
		'Region',
		related_name="int_second_region_purchase_slaves",
		verbose_name="Second intended region of purchase of slaves (EMBREG2)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	int_first_port_dis = models.ForeignKey(
		'Place',
		related_name="int_first_port_dis",
		verbose_name="First intended port of disembarkation (ARRPORT)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	int_second_port_dis = models.ForeignKey(
		'Place',
		related_name="int_second_port_dis",
		verbose_name="Second intended port of disembarkation (ARRPORT2)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	int_first_region_slave_landing = models.ForeignKey(
		'Region',
		related_name="int_first_region_slave_landing",
		verbose_name="First intended region of slave landing (REGARR)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	# variable name should be changed from int_second_place_region_slave_landing to int_second_region_slave_landing.  	
	int_second_place_region_slave_landing = models.ForeignKey(
		'Region',
		related_name="int_second_region_slave_landing",
		verbose_name="Second intended region of slave landing (REGARR2)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)

	# End of intended variables
	ports_called_buying_slaves = models.IntegerField(
		"Number of ports of call prior to buying slaves (NPPRETRA)",
		null=True,
		blank=True)

	first_place_slave_purchase = models.ForeignKey(
		'Place',
		related_name="first_place_slave_purchase",
		verbose_name="First place of slave purchase (PLAC1TRA)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	second_place_slave_purchase = models.ForeignKey(
		'Place',
		related_name="second_place_slave_purchase",
		verbose_name="Second place of slave purchase (PLAC2TRA)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	third_place_slave_purchase = models.ForeignKey(
		'Place',
		related_name="third_place_slave_purchase",
		verbose_name="Third place of slave purchase (PLAC3TRA)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)

	first_region_slave_emb = models.ForeignKey(
		'Region',
		related_name="first_region_slave_emb",
		verbose_name="First region of embarkation of slaves (REGEM1)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	second_region_slave_emb = models.ForeignKey(
		'Region',
		related_name="second_region_slave_emb",
		verbose_name="Second region of embarkation of slaves (REGEM2)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	third_region_slave_emb = models.ForeignKey(
		'Region',
		related_name="third_region_slave_emb",
		verbose_name="Third region of embarkation of slaves (REGEM3)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)

	port_of_call_before_atl_crossing = models.ForeignKey(
		'Place',
		related_name="port_of_call_before_atl_crossing",
		verbose_name="Port of call before Atlantic crossing (NPAFTTRA)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)

	number_of_ports_of_call = models.IntegerField(
		"Number of ports of call in Americas prior to sale of slaves "
		"(NPPRIOR)",
		null=True,
		blank=True)
	first_landing_place = models.ForeignKey(
		'Place',
		related_name="first_landing_place",
		verbose_name="First place of slave landing (SLA1PORT)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	second_landing_place = models.ForeignKey(
		'Place',
		related_name="second_landing_place",
		verbose_name="Second place of slave landing (ADPSALE1)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	third_landing_place = models.ForeignKey(
		'Place',
		related_name="third_landing_place",
		verbose_name="Third place of slave landing (ADPSALE2)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)

	first_landing_region = models.ForeignKey(
		'Region',
		related_name="first_landing_region",
		verbose_name="First region of slave landing (REGDIS1)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	second_landing_region = models.ForeignKey(
		'Region',
		related_name="second_landing_region",
		verbose_name="Second region of slave landing (REGDIS2)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	third_landing_region = models.ForeignKey(
		'Region',
		related_name="third_landing_region",
		verbose_name="Third region of slave landing (REGDIS3)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)

	place_voyage_ended = models.ForeignKey(
		'Place',
		related_name="place_voyage_ended",
		verbose_name="Place at which voyage ended (PORTRET)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	region_of_return = models.ForeignKey(
		'Region',
		related_name="region_of_return",
		verbose_name="Region of return (RETRNREG)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	broad_region_of_return = models.ForeignKey(
		'BroadRegion',
		related_name="broad_region_of_return",
		verbose_name="Broad region of return (RETRNREG1)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)

	# Imputed variables
	imp_port_voyage_begin = models.ForeignKey(
		'Place',
		related_name="imp_port_voyage_begin",
		verbose_name="Imputed port where voyage began (PTDEPIMP)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	imp_region_voyage_begin = models.ForeignKey(
		'Region',
		related_name="imp_region_voyage_begin",
		verbose_name="Imputed region where voyage began (DEPTREGIMP)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	imp_broad_region_voyage_begin = models.ForeignKey(
		'BroadRegion',
		related_name="imp_broad_region_voyage_begin",
		verbose_name="Imputed broad region where voyage began (DEPTREGIMP1)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	principal_place_of_slave_purchase = models.ForeignKey(
		'Place',
		related_name="principal_place_of_slave_purchase",
		verbose_name="Principal place of slave purchase (MAJBUYPT)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	imp_principal_place_of_slave_purchase = models.ForeignKey(
		'Place',
		related_name="imp_principal_place_of_slave_purchase",
		verbose_name="Imputed principal place of slave purchase (MJBYPTIMP)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	imp_principal_region_of_slave_purchase = models.ForeignKey(
		'Region',
		related_name="imp_principal_region_of_slave_purchase",
		verbose_name="Imputed principal region of slave purchase (MAJBYIMP)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	imp_broad_region_of_slave_purchase = models.ForeignKey(
		'BroadRegion',
		related_name="imp_broad_region_of_slave_purchase",
		verbose_name="Imputed principal broad region of slave purchase "
		"(MAJBYIMP1)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	principal_port_of_slave_dis = models.ForeignKey(
		'Place',
		related_name="principal_port_of_slave_dis",
		verbose_name="Principal port of slave disembarkation (MAJSELPT)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	imp_principal_port_slave_dis = models.ForeignKey(
		'Place',
		related_name="imp_principal_port_slave_dis",
		verbose_name="Imputed principal port of slave disembarkation "
		"(MJSLPTIMP)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	imp_principal_region_slave_dis = models.ForeignKey(
		'Region',
		related_name="imp_principal_region_slave_dis",
		verbose_name="Imputed principal region of slave disembarkation "
		"(MJSELIMP)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)
	imp_broad_region_slave_dis = models.ForeignKey(
		'BroadRegion',
		related_name="imp_broad_region_slave_dis",
		verbose_name="Imputed broad region of slave disembarkation "
		"(MJSELIMP1)",
		null=True,
		blank=True,
		on_delete=models.CASCADE)

	voyage = models.ForeignKey('Voyage',
							   null=True,
							   blank=True,
							   on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Itinerary"
		verbose_name_plural = "Itineraries"


# Voyage Dates
class VoyageDates(models.Model):
	"""
	Voyage dates.
	"""

	# Constant variables
	# Dates start
	years_start = {5: 1525, 10: 1500, 25: 1500, 100: 1500}

	# Data variables
	voyage_began = models.CharField(
		"Date that voyage began (DATEDEPB,A,C)",
		max_length=10,
		blank=True,
		null=True,
		help_text="Date in format: MM,DD,YYYY")
	voyage_began_mm = models.IntegerField(
		"Month that voyage began (DATEDEPB,A,C)",
		blank=True,
		null=True,
		help_text="Month in format: MM,DD,YYYY")
	voyage_began_dd = models.IntegerField(
		"Day that voyage began (DATEDEPB,A,C)",
		blank=True,
		null=True,
		help_text="Day in format: MM,DD,YYYY")
	voyage_began_yyyy = models.IntegerField(
		"Year that voyage began (DATEDEPB,A,C)",
		blank=True,
		null=True,
		help_text="Year in format: MM,DD,YYYY")

	slave_purchase_began = models.CharField(
		"Date that slave purchase began (D1SLATRB,A,C)",
		max_length=10,
		blank=True,
		null=True,
		help_text="Date in format: MM,DD,YYYY")
	slave_purchase_began_mm = models.IntegerField(
		"Month that slave purchase began (D1SLATRB,A,C)",
		blank=True,
		null=True,
		help_text="Month in format: MM,DD,YYYY")
	slave_purchase_began_dd = models.IntegerField(
		"Day that slave purchase began (D1SLATRB,A,C)",
		blank=True,
		null=True,
		help_text="Day in format: MM,DD,YYYY")
	slave_purchase_began_yyyy = models.IntegerField(
		"Year that slave purchase began (D1SLATRB,A,C)",
		blank=True,
		null=True,
		help_text="Year in format: MM,DD,YYYY")

	vessel_left_port = models.CharField(
		"Date that vessel left last slaving port (DLSLATRB,A,C)",
		max_length=10,
		blank=True,
		null=True,
		help_text="Date in format: MM,DD,YYYY")
	vessel_left_port_mm = models.IntegerField(
		"Month that vessel left last slaving port (DLSLATRB,A,C)",
		blank=True,
		null=True,
		help_text="Month in format: MM,DD,YYYY")
	vessel_left_port_dd = models.IntegerField(
		"Day that vessel left last slaving port (DLSLATRB,A,C)",
		blank=True,
		null=True,
		help_text="Day in format: MM,DD,YYYY")
	vessel_left_port_yyyy = models.IntegerField(
		"Year that vessel left last slaving port (DLSLATRB,A,C)",
		blank=True,
		null=True,
		help_text="Year in format: MM,DD,YYYY")

	first_dis_of_slaves = models.CharField(
		"Date of first disembarkation of slaves (DATARR33,32,34)",
		max_length=10,
		blank=True,
		null=True,
		help_text="Date in format: MM,DD,YYYY")
	first_dis_of_slaves_mm = models.IntegerField(
		"Month of first disembarkation of slaves (DATARR33,32,34)",
		blank=True,
		null=True,
		help_text="Month in format: MM,DD,YYYY")
	first_dis_of_slaves_dd = models.IntegerField(
		"Day of first disembarkation of slaves (DATARR33,32,34)",
		blank=True,
		null=True,
		help_text="Day in format: MM,DD,YYYY")
	first_dis_of_slaves_yyyy = models.IntegerField(
		"Year of first disembarkation of slaves (DATARR33,32,34)",
		blank=True,
		null=True,
		help_text="Year in format: MM,DD,YYYY")

	date_departed_africa = models.CharField(
		"Date vessel departed Africa (DATELEFTAFR)",
		max_length=10,
		blank=True,
		null=True,
		help_text="Date in format: MM,DD,YYYY")
	date_departed_africa_mm = models.IntegerField(
		"Month vessel departed Africa (DATELEFTAFR)",
		blank=True,
		null=True,
		help_text="Month in format: MM,DD,YYYY")
	date_departed_africa_dd = models.IntegerField(
		"Day vessel departed Africa (DATELEFTAFR)",
		blank=True,
		null=True,
		help_text="Day in format: MM,DD,YYYY")
	date_departed_africa_yyyy = models.IntegerField(
		"Year vessel departed Africa (DATELEFTAFR)",
		blank=True,
		null=True,
		help_text="Year in format: MM,DD,YYYY")

	arrival_at_second_place_landing = models.CharField(
		"Date of arrival at second place of landing (DATARR37,36,38)",
		max_length=10,
		blank=True,
		null=True,
		help_text="Date in format: MM,DD,YYYY")
	arrival_at_second_place_landing_mm = models.IntegerField(
		"Month of arrival at second place of landing (DATARR37,36,38)",
		blank=True,
		null=True,
		help_text="Month in format: MM,DD,YYYY")
	arrival_at_second_place_landing_dd = models.IntegerField(
		"Day of arrival at second place of landing (DATARR37,36,38)",
		blank=True,
		null=True,
		help_text="Day in format: MM,DD,YYYY")
	arrival_at_second_place_landing_yyyy = models.IntegerField(
		"Year of arrival at second place of landing (DATARR37,36,38)",
		blank=True,
		null=True,
		help_text="Year in format: MM,DD,YYYY")

	third_dis_of_slaves = models.CharField(
		"Date of third disembarkation of slaves (DATARR40,39,41)",
		max_length=10,
		blank=True,
		null=True,
		help_text="Date in format: MM,DD,YYYY")
	third_dis_of_slaves_mm = models.IntegerField(
		"Month of third disembarkation of slaves (DATARR40,39,41)",
		blank=True,
		null=True,
		help_text="Month in format: MM,DD,YYYY")
	third_dis_of_slaves_dd = models.IntegerField(
		"Day of third disembarkation of slaves (DATARR40,39,41)",
		blank=True,
		null=True,
		help_text="Day in format: MM,DD,YYYY")
	third_dis_of_slaves_yyyy = models.IntegerField(
		"Year of third disembarkation of slaves (DATARR40,39,41)",
		blank=True,
		null=True,
		help_text="Year in format: MM,DD,YYYY")

	departure_last_place_of_landing = models.CharField(
		"Date of departure from last place of landing (DDEPAMB,*,C)",
		max_length=10,
		blank=True,
		null=True,
		help_text="Date in format: MM,DD,YYYY")
	departure_last_place_of_landing_mm = models.IntegerField(
		"Month of departure from last place of landing (DDEPAMB,*,C)",
		blank=True,
		null=True,
		help_text="Month in format: MM,DD,YYYY")
	departure_last_place_of_landing_dd = models.IntegerField(
		"Day of departure from last place of landing (DDEPAMB,*,C)",
		blank=True,
		null=True,
		help_text="Day in format: MM,DD,YYYY")
	departure_last_place_of_landing_yyyy = models.IntegerField(
		"Year of departure from last place of landing (DDEPAMB,*,C)",
		blank=True,
		null=True,
		help_text="Year in format: MM,DD,YYYY")

	voyage_completed = models.CharField(
		"Date on which slave voyage completed (DATARR44,43,45)",
		max_length=10,
		blank=True,
		null=True,
		help_text="Date in format: MM,DD,YYYY")
	voyage_completed_mm = models.IntegerField(
		"Month on which slave voyage completed (DATARR44,43,45)",
		blank=True,
		null=True,
		help_text="Month in format: MM,DD,YYYY")
	voyage_completed_dd = models.IntegerField(
		"Day on which slave voyage completed (DATARR44,43,45)",
		blank=True,
		null=True,
		help_text="Day in format: MM,DD,YYYY")
	voyage_completed_yyyy = models.IntegerField(
		"Year on which slave voyage completed (DATARR44,43,45)",
		blank=True,
		null=True,
		help_text="Year in format: MM,DD,YYYY")

	# Later this can become just a property/ can be calculated
	length_middle_passage_days = models.IntegerField(
		"Length of Middle Passage in (days) (VOYAGE)", null=True, blank=True)

	# Imputed variables
	imp_voyage_began = models.CharField("Year voyage began",
										max_length=10,
										blank=True,
										null=True,
										help_text="Date in format: MM,DD,YYYY")
	imp_voyage_began_yyyy = models.IntegerField("Year voyage began",
										blank=True,
										null=True,
										help_text="Date in format: YYYY")
	
	imp_departed_africa = models.CharField(
		"Year departed Africa",
		max_length=10,
		blank=True,
		null=True,
		help_text="Date in format: MM,DD,YYYY")
	imp_departed_africa_yyyy = models.IntegerField(
		"Year departed Africa",
		blank=True,
		null=True,
		help_text="Date in format: YYYY")
		
	imp_arrival_at_port_of_dis = models.CharField(
		"Year of arrival at port of disembarkation (YEARAM)",
		max_length=10,
		blank=True,
		null=True,
		help_text="Date in format: MM,DD,YYYY")
	imp_arrival_at_port_of_dis_yyyy = models.IntegerField(
		"Year of arrival at port of disembarkation (YEARAM)",
		blank=True,
		null=True,
		help_text="Date in format: YYYY")

	# Later this can become just a property/ can be calculated
	imp_length_home_to_disembark = models.IntegerField(
		"Voyage length from home port to disembarkation (days) (VOY1IMP)",
		null=True,
		blank=True)
		
	imp_length_leaving_africa_to_disembark = models.IntegerField(
		"Voyage length from last slave embarkation to first disembarkation "
		"(days) (VOY2IMP)",
		null=True,
		blank=True)

	voyage = models.ForeignKey('Voyage',
							   null=True,
							   blank=True,
							   on_delete=models.CASCADE)
	
	def __str__(self):
		return self.imp_arrival_at_port_of_dis
	
	@classmethod
	def get_date_year(cls, value):
		"""
		Returns year value from CommaSeparatedField, or None if undefined
		"""
		if not value:
			return None
		strval = value.split(',')[2]
		if len(strval) < 1:
			return None
		try:
			return int(strval)
		except Exception:
			return None

	@classmethod
	def get_date_month(cls, value):
		"""
		Returns month value from CommaSeparatedField, or 0 if undefined
		"""
		if not value:
			return 0
		strval = value.split(',')[1]
		if len(strval) < 1:
			return 0
		try:
			return int(strval)
		except Exception:
			return None

	@classmethod
	def get_date_day(cls, value):
		"""
		Returns date value from CommaSeparatedField, or 0 if undefined
		"""
		if not value:
			return 0
		strval = value.split(',')[0]
		if len(strval) < 1:
			return 0
		try:
			return int(strval)
		except Exception:
			return None

	# don't think this is being used anywhere
#	def calculate_year_period(self, period):
#		"""
#		Function to calculate proper period.
#
#		Keyword arguments:
#		period -- which period to calculate
#		"""
#
#		if (period != 100):
#			if ((self.get_date_year(self.imp_arrival_at_port_of_dis) -
#			self.years_start[period]) % period != 0):
#				return ((self.get_date_year(self.imp_arrival_at_port_of_dis) -
#				self.years_start[period]) / period +1)
#			else:
#				return
#				(self.get_date_year(self.imp_arrival_at_port_of_dis) -
#				self.years_start[period]) \ / period
#		else:
#			return ((self.get_date_year(self.imp_arrival_at_port_of_dis))/100
#			+ 100)

	class Meta:
		verbose_name = "Date"
		verbose_name_plural = "Dates"


# Voyage Captain and Crew
class VoyageCaptain(models.Model):
	"""
	Voyage Captain and Crew.
	"""
	name = models.CharField("Captain's name", max_length=255)

	class Meta:
		verbose_name = "Captain"
		verbose_name_plural = "Captains"
		
	def __str__(self):
		return self.name


class VoyageCaptainConnection(models.Model):
	"""
	Represents the relation between Voyage Captain and
	Voyage.
	captain_order represents order of each captain (1st, 2nd, ...)
	related to: :class:`~voyages.apps.voyage.models.VoyageCaptain`
	related to: :class:`~voyages.apps.voyage.models.Voyage`
	"""

	captain = models.ForeignKey('VoyageCaptain',
								on_delete=models.CASCADE,)
	voyage = models.ForeignKey('Voyage',
							   on_delete=models.CASCADE,
							   related_name='voyage_captainconnection')
	captain_order = models.IntegerField()

	class Meta:
		verbose_name = "Voyage captain information"
		verbose_name_plural = "Voyage captain information"

	def __str__(self):
		return "Captain: %d %s" % (self.captain_order, str(self.captain))



class VoyageCrew(models.Model):
	"""
	Voyage Crew.
	related to: :class:`~voyages.apps.voyage.models.Voyage`
	"""

	crew_voyage_outset = models.IntegerField("Crew at voyage outset",
											 null=True,
											 blank=True)
	crew_departure_last_port = models.IntegerField(
		"Crew at departure from last port of slave purchase",
		null=True,
		blank=True)
	crew_first_landing = models.IntegerField("Crew at first landing of slaves",
											 null=True,
											 blank=True)
	crew_return_begin = models.IntegerField("Crew when return voyage begin",
											null=True,
											blank=True)
	crew_end_voyage = models.IntegerField("Crew at end of voyage",
										  null=True,
										  blank=True)
	unspecified_crew = models.IntegerField("Number of crew unspecified",
										   null=True,
										   blank=True)
	crew_died_before_first_trade = models.IntegerField(
		"Crew died before first place of trade in Africa",
		null=True,
		blank=True)
	crew_died_while_ship_african = models.IntegerField(
		"Crew died while ship was on African coast", null=True, blank=True)
	crew_died_middle_passage = models.IntegerField(
		"Crew died during Middle Passage", null=True, blank=True)
	crew_died_in_americas = models.IntegerField("Crew died in the Americas",
												null=True,
												blank=True)
	crew_died_on_return_voyage = models.IntegerField(
		"Crew died on return voyage", null=True, blank=True)
	crew_died_complete_voyage = models.IntegerField(
		"Crew died during complete voyage", null=True, blank=True)
	crew_deserted = models.IntegerField("Total number of crew deserted",
										null=True,
										blank=True)

	voyage = models.ForeignKey('Voyage',
							   null=True,
							   blank=True,
							   on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Crew"
		verbose_name_plural = "Crews"


# Voyage Slaves (numbers)
class VoyageSlavesNumbers(models.Model):
	"""
	Voyage slaves (numbers).
	related to: :class:`~voyages.apps.voyage.models.Voyage`
	"""

	slave_deaths_before_africa = models.IntegerField(
		"Slaves death before leaving Africa (SLADAFRI)", null=True, blank=True)
	slave_deaths_between_africa_america = models.IntegerField(
		"Slaves death between Africa and Americas (SLADVOY)",
		null=True,
		blank=True)
	slave_deaths_between_arrival_and_sale = models.IntegerField(
		"Slaves death before arrival and sale (SLADAMER)",
		null=True,
		blank=True)
	num_slaves_intended_first_port = models.IntegerField(
		"Number of slaves intended from first port of purchase "
		"(SLINTEND)",
		null=True,
		blank=True)
	num_slaves_intended_second_port = models.IntegerField(
		"Number of slaves intended from second port of purchase "
		"(SLINTEN2)",
		null=True,
		blank=True)

	num_slaves_carried_first_port = models.IntegerField(
		"Number of slaves carried from first port of purchase "
		"(NCAR13)",
		null=True,
		blank=True)
	num_slaves_carried_second_port = models.IntegerField(
		"Number of slaves carried from second port of purchase "
		"(NCAR15)",
		null=True,
		blank=True)
	num_slaves_carried_third_port = models.IntegerField(
		"Number of slaves carried from third port of purchase "
		"(NCAR17)",
		null=True,
		blank=True)

	total_num_slaves_purchased = models.IntegerField(
		"Total slaves purchased (TSLAVESP)", null=True, blank=True)
	total_num_slaves_dep_last_slaving_port = models.IntegerField(
		"Total slaves on board at departure from last slaving port "
		"(TSLAVESD)",
		null=True,
		blank=True)

	total_num_slaves_arr_first_port_embark = models.IntegerField(
		"Total slaves arrived at first port of disembarkation "
		"(SLAARRIV)",
		null=True,
		blank=True)

	num_slaves_disembark_first_place = models.IntegerField(
		"Number of slaves disembarked at first place "
		"(SLAS32)",
		null=True,
		blank=True)
	num_slaves_disembark_second_place = models.IntegerField(
		"Number of slaves disembarked at second place "
		"(SLAS36)",
		null=True,
		blank=True)
	num_slaves_disembark_third_place = models.IntegerField(
		"Number of slaves disembarked at third place "
		"(SLAS39)",
		null=True,
		blank=True)

	# Imputed variables
	imp_total_num_slaves_embarked = models.IntegerField(
		"Total slaves embarked imputed * "
		"(slaximp)", null=True, blank=True)

	imp_total_num_slaves_disembarked = models.IntegerField(
		"Total slaves disembarked imputed * "
		"(SLAMIMP)",
		null=True,
		blank=True)

	imp_jamaican_cash_price = models.DecimalField(
		"Sterling cash price in Jamaica* (imputed)",
		null=True,
		blank=True,
		max_digits=10,
		decimal_places=4)

	imp_mortality_during_voyage = models.IntegerField(
		"Imputed number of slave deaths during Middle Passage "
		"(VYMRTIMP)",
		null=True,
		blank=True)

	# Voyage characteristics

	# Representing MEN1 variables
	num_men_embark_first_port_purchase = models.IntegerField(
		"Number of men (MEN1) embarked at first port of purchase",
		null=True,
		blank=True)
	# Representing WOMEN1 variables
	num_women_embark_first_port_purchase = models.IntegerField(
		"Number of women (WOMEN1) embarked at first port of purchase",
		null=True,
		blank=True)
	# Representing BOY1 variables
	num_boy_embark_first_port_purchase = models.IntegerField(
		"Number of boys (BOY1) embarked at first port of purchase",
		null=True,
		blank=True)
	# Representing GIRL1 variables
	num_girl_embark_first_port_purchase = models.IntegerField(
		"Number of girls (GIRL1) embarked at first port of purchase",
		null=True,
		blank=True)
	# Representing ADULT1 variables
	num_adult_embark_first_port_purchase = models.IntegerField(
		"Number of adults (gender unspecified) (ADULT1) "
		"embarked at first port of purchase",
		null=True,
		blank=True)
	# Representing CHILD1 variables
	num_child_embark_first_port_purchase = models.IntegerField(
		"Number of children (gender unspecified) (CHILD1) "
		"embarked at first port of purchase",
		null=True,
		blank=True)
	# Representing INFANT1 variables
	num_infant_embark_first_port_purchase = models.IntegerField(
		"Number of infants (INFANT1) embarked at first port of purchase",
		null=True,
		blank=True)
	# Representing MALE1 variables
	num_males_embark_first_port_purchase = models.IntegerField(
		"Number of males (age unspecified) (MALE1)"
		" embarked at first port of purchase",
		null=True,
		blank=True)
	# Representing FEMALE1 variables
	num_females_embark_first_port_purchase = models.IntegerField(
		"Number of females (age unspecified) (FEMALE1) "
		"embarked at first port of purchase",
		null=True,
		blank=True)

	# Representing MEN2 variables
	num_men_died_middle_passage = models.IntegerField(
		"Number of men (MEN2) died on Middle Passage", null=True, blank=True)
	# Representing WOMEN2 variables
	num_women_died_middle_passage = models.IntegerField(
		"Number of women (WOMEN2) died on Middle Passage",
		null=True,
		blank=True)
	# Representing BOY2 variables
	num_boy_died_middle_passage = models.IntegerField(
		"Number of boys (BOY2) died on Middle Passage", null=True, blank=True)
	# Representing GIRL2 variables
	num_girl_died_middle_passage = models.IntegerField(
		"Number of girls (GIRL2) died on Middle Passage",
		null=True, blank=True)
	# Representing ADULT2 variables
	num_adult_died_middle_passage = models.IntegerField(
		"Number of adults (gender unspecified) (ADULT2) "
		"died on Middle Passage",
		null=True,
		blank=True)
	# Representing CHILD2 variables
	num_child_died_middle_passage = models.IntegerField(
		"Number of children (gender unspecified) (CHILD2) "
		"died on Middle Passage",
		null=True,
		blank=True)
	# Representing INFANT2 variables
	num_infant_died_middle_passage = models.IntegerField(
		"Number of infants (INFANT2) died on Middle Passage",
		null=True,
		blank=True)
	# Representing MALE2 variables
	num_males_died_middle_passage = models.IntegerField(
		"Number of males (age unspecified) (MALE2) "
		"died on Middle Passage",
		null=True,
		blank=True)
	# Representing FEMALE2 variables
	num_females_died_middle_passage = models.IntegerField(
		"Number of females (age unspecified) (FEMALE2) "
		"died on Middle Passage",
		null=True,
		blank=True)

	# Representing MEN3 variables
	num_men_disembark_first_landing = models.IntegerField(
		"Number of men (MEN3) disembarked at first place of landing",
		null=True,
		blank=True)
	# Representing WOMEN3 variables
	num_women_disembark_first_landing = models.IntegerField(
		"Number of women (WOMEN3) disembarked at first place of landing",
		null=True,
		blank=True)
	# Representing BOY3 variables
	num_boy_disembark_first_landing = models.IntegerField(
		"Number of boys (BOY3) disembarked at first place of landing",
		null=True,
		blank=True)
	# Representing GIRL3 variables
	num_girl_disembark_first_landing = models.IntegerField(
		"Number of girls (GIRL3) disembarked at first place of landing",
		null=True,
		blank=True)
	# Representing ADULT3 variables
	num_adult_disembark_first_landing = models.IntegerField(
		"Number of adults (gender unspecified) (ADULT3) "
		"disembarked at first place of landing",
		null=True,
		blank=True)
	# Representing CHILD3 variables
	num_child_disembark_first_landing = models.IntegerField(
		"Number of children (gender unspecified) (CHILD3) "
		"disembarked at first place of landing",
		null=True,
		blank=True)
	# Representing INFANT3 variables
	num_infant_disembark_first_landing = models.IntegerField(
		"Number of infants (INFANT3) disembarked "
		"at first place of landing",
		null=True,
		blank=True)
	# Representing MALE3 variables
	num_males_disembark_first_landing = models.IntegerField(
		"Number of males (age unspecified) (MALE3) "
		"disembarked at first place of landing",
		null=True,
		blank=True)
	# Representing FEMALE3 variables
	num_females_disembark_first_landing = models.IntegerField(
		"Number of females (age unspecified) (FEMALE3) "
		"disembarked at first place of landing",
		null=True,
		blank=True)

	# Representing MEN4 variables
	num_men_embark_second_port_purchase = models.IntegerField(
		"Number of men (MEN4) embarked at second port of purchase",
		null=True,
		blank=True)
	# Representing WOMEN4 variables
	num_women_embark_second_port_purchase = models.IntegerField(
		"Number of women (WOMEN4) embarked at second port of purchase",
		null=True,
		blank=True)
	# Representing BOY4 variables
	num_boy_embark_second_port_purchase = models.IntegerField(
		"Number of boys (BOY4) embarked at second port of purchase",
		null=True,
		blank=True)
	# Representing GIRL4 variables
	num_girl_embark_second_port_purchase = models.IntegerField(
		"Number of girls (GIRL4) embarked at second port of purchase",
		null=True,
		blank=True)
	# Representing ADULT4 variables
	num_adult_embark_second_port_purchase = models.IntegerField(
		"Number of adults (gender unspecified) (ADULT4) "
		"embarked at second port of purchase",
		null=True,
		blank=True)
	# Representing CHILD4 variables
	num_child_embark_second_port_purchase = models.IntegerField(
		"Number of children (gender unspecified) (CHILD4) "
		"embarked at second port of purchase",
		null=True,
		blank=True)
	# Representing INFANT4 variables
	num_infant_embark_second_port_purchase = models.IntegerField(
		"Number of infants (INFANT4) embarked "
		"at second port of purchase",
		null=True,
		blank=True)
	# Representing MALE4 variables
	num_males_embark_second_port_purchase = models.IntegerField(
		"Number of males (age unspecified) (MALE4) "
		"embarked at second port of purchase",
		null=True,
		blank=True)
	# Representing FEMALE4 variables
	num_females_embark_second_port_purchase = models.IntegerField(
		"Number of females (age unspecified) (FEMALE4) "
		"embarked at second port of purchase",
		null=True,
		blank=True)

	# Representing MEN5 variables
	num_men_embark_third_port_purchase = models.IntegerField(
		"Number of men (MEN5) embarked at third port of purchase",
		null=True,
		blank=True)
	# Representing WOMEN5 variables
	num_women_embark_third_port_purchase = models.IntegerField(
		"Number of women (WOMEN5) embarked at third port of purchase",
		null=True,
		blank=True)
	# Representing BOY5 variables
	num_boy_embark_third_port_purchase = models.IntegerField(
		"Number of boys (BOY5) embarked at third port of purchase",
		null=True,
		blank=True)
	# Representing GIRL5 variables
	num_girl_embark_third_port_purchase = models.IntegerField(
		"Number of girls (GIRL5) embarked at third port of purchase",
		null=True,
		blank=True)
	# Representing ADULT5 variables
	num_adult_embark_third_port_purchase = models.IntegerField(
		"Number of adults (gender unspecified) (ADULT5) "
		"embarked at third port of purchase",
		null=True,
		blank=True)
	# Representing CHILD5 variables
	num_child_embark_third_port_purchase = models.IntegerField(
		"Number of children (gender unspecified) (CHILD5) "
		"embarked at third port of purchase",
		null=True,
		blank=True)
	# Representing INFANT5 variables
	num_infant_embark_third_port_purchase = models.IntegerField(
		"Number of infants (INFANT5) embarked at third port of purchase",
		null=True,
		blank=True)
	# Representing MALE5 variables
	num_males_embark_third_port_purchase = models.IntegerField(
		"Number of males (age unspecified) (MALE5) embarked "
		"at third port of purchase",
		null=True,
		blank=True)
	# Representing FEMALE5 variables
	num_females_embark_third_port_purchase = models.IntegerField(
		"Number of females (age unspecified) (FEMALE5) embarked "
		"at third port of purchase",
		null=True,
		blank=True)

	# Representing MEN6 variables
	num_men_disembark_second_landing = models.IntegerField(
		"Number of men (MEN6) disembarked at second place of landing",
		null=True,
		blank=True)
	# Representing WOMEN6 variables
	num_women_disembark_second_landing = models.IntegerField(
		"Number of women (WOMEN6) disembarked "
		"at second place of landing",
		null=True,
		blank=True)
	# Representing BOY6 variables
	num_boy_disembark_second_landing = models.IntegerField(
		"Number of boys (BOY6) disembarked at second place of landing",
		null=True,
		blank=True)
	# Representing GIRL6 variables
	num_girl_disembark_second_landing = models.IntegerField(
		"Number of girls (GIRL6) disembarked at second place of landing",
		null=True,
		blank=True)
	# Representing ADULT6 variables
	num_adult_disembark_second_landing = models.IntegerField(
		"Number of adults (gender unspecified) (ADULT6) disembarked "
		"at second place of landing",
		null=True,
		blank=True)
	# Representing CHILD6 variables
	num_child_disembark_second_landing = models.IntegerField(
		"Number of children (gender unspecified) (CHILD6) "
		"disembarked at second place of landing",
		null=True,
		blank=True)
	# Representing INFANT6 variables
	num_infant_disembark_second_landing = models.IntegerField(
		"Number of infants (INFANT6) disembarked "
		"at second place of landing",
		null=True,
		blank=True)
	# Representing MALE6 variables
	num_males_disembark_second_landing = models.IntegerField(
		"Number of males (age unspecified) (MALE6) "
		"disembarked at second place of landing",
		null=True,
		blank=True)
	# Representing FEMALE6 variables
	num_females_disembark_second_landing = models.IntegerField(
		"Number of females (age unspecified) (FEMALE6) "
		"disembarked at second place of landing",
		null=True,
		blank=True)

	# Imputed slave characteristics
	imp_num_adult_embarked = models.IntegerField(
		"Imputed number of adults embarked (ADLT1IMP)", null=True, blank=True)
	imp_num_children_embarked = models.IntegerField(
		"Imputed number of adults embarked (CHIL1IMP)", null=True, blank=True)
	imp_num_male_embarked = models.IntegerField(
		"Imputed number of males embarked (MALE1IMP)", null=True, blank=True)
	imp_num_female_embarked = models.IntegerField(
		"Imputed number of females embarked (FEML1IMP)", null=True, blank=True)
	total_slaves_embarked_age_identified = models.IntegerField(
		"Total slaves embarked with age identified (SLAVEMA1)",
		null=True,
		blank=True)
	total_slaves_embarked_gender_identified = models.IntegerField(
		"Total slaves embarked with gender identified (SLAVEMX1)",
		null=True,
		blank=True)

	imp_adult_death_middle_passage = models.IntegerField(
		"Imputed number of adults who died on Middle Passage (ADLT2IMP)",
		null=True,
		blank=True)
	imp_child_death_middle_passage = models.IntegerField(
		"Imputed number of children who died on Middle Passage (CHIL2IMP)",
		null=True,
		blank=True)
	imp_male_death_middle_passage = models.IntegerField(
		"Imputed number of males who died on Middle Passage (MALE2IMP)",
		null=True,
		blank=True)
	imp_female_death_middle_passage = models.IntegerField(
		"Imputed number of females who died on Middle Passage (FEML2IMP)",
		null=True,
		blank=True)
	imp_num_adult_landed = models.IntegerField(
		"Imputed number of adults landed (ADLT3IMP)", null=True, blank=True)
	imp_num_child_landed = models.IntegerField(
		"Imputed number of children landed (CHIL3IMP)", null=True, blank=True)
	imp_num_male_landed = models.IntegerField(
		"Imputed number of males landed (MALE3IMP)", null=True, blank=True)
	imp_num_female_landed = models.IntegerField(
		"Imputed number of females landed (FEML3IMP)", null=True, blank=True)
	total_slaves_landed_age_identified = models.IntegerField(
		"Total slaves identified by age among landed slaves (SLAVEMA3)",
		null=True,
		blank=True)
	total_slaves_landed_gender_identified = models.IntegerField(
		"Total slaves identified by gender among landed slaves (SLAVEMX3)",
		null=True,
		blank=True)
	total_slaves_dept_or_arr_age_identified = models.IntegerField(
		"Total slaves identified by age at departure or arrival (SLAVEMA7)",
		null=True,
		blank=True)
	total_slaves_dept_or_arr_gender_identified = models.IntegerField(
		"Total slaves identified by gender at departure or arrival(SLAVEMX7)",
		null=True,
		blank=True)
	imp_slaves_embarked_for_mortality = models.IntegerField(
		"Imputed number of slaves embarked for mortality calculation "
		"(TSLMTIMP)",
		null=True,
		blank=True)

	# Representing MEN7 variables
	imp_num_men_total = models.IntegerField("Number of men (MEN7)",
											null=True,
											blank=True)
	# Representing WOMEN7 variables
	imp_num_women_total = models.IntegerField("Number of women (WOMEN7) ",
											  null=True,
											  blank=True)
	# Representing BOY7 variables
	imp_num_boy_total = models.IntegerField("Number of boys (BOY7)",
											null=True,
											blank=True)
	# Representing GIRL7 variables
	imp_num_girl_total = models.IntegerField("Number of girls (GIRL7)",
											 null=True,
											 blank=True)
	# Representing ADULT7 variables
	imp_num_adult_total = models.IntegerField(
		"Number of adults (gender unspecified) (ADULT7)",
		null=True, blank=True)
	# Representing CHILD7 variables
	imp_num_child_total = models.IntegerField(
		"Number of children (gender unspecified) (CHILD7)",
		null=True,
		blank=True)

	# Representing MALE7 variables
	imp_num_males_total = models.IntegerField(
		"Number of males (age unspecified) (MALE7)", null=True, blank=True)
	# Representing FEMALE7 variables
	imp_num_females_total = models.IntegerField(
		"Number of females (age unspecified) (FEMALE7) ",
		null=True, blank=True)

	total_slaves_embarked_age_gender_identified = models.IntegerField(
		"Total slaves embarked wi th age and gender identified (SLAVMAX1)",
		null=True,
		blank=True)
	total_slaves_by_age_gender_identified_among_landed = models.IntegerField(
		"Total slaves identified by age and gender among landed (SLAVMAX3)",
		null=True,
		blank=True)
	total_slaves_by_age_gender_identified_departure_or_arrival = (
		models.IntegerField(
			"Total slaves identified by age and gender at departure or "
			"arrival (SLAVMAX7)",
			null=True, blank=True))

	percentage_boys_among_embarked_slaves = models.FloatField(
		"Percentage of boys among embarked slaves (BOYRAT1)",
		null=True,
		blank=True)

	child_ratio_among_embarked_slaves = models.FloatField(
		"Child ratio among embarked slaves (CHILRAT1)", null=True, blank=True)

	percentage_girls_among_embarked_slaves = models.FloatField(
		"Percentage of girls among embarked slaves (GIRLRAT1)",
		null=True,
		blank=True)

	male_ratio_among_embarked_slaves = models.FloatField(
		"Male ratio among embarked slaves (MALRAT1)", null=True, blank=True)

	percentage_men_among_embarked_slaves = models.FloatField(
		"Percentage of men among embarked slaves (MENRAT1)",
		null=True,
		blank=True)

	percentage_women_among_embarked_slaves = models.FloatField(
		"Percentage of women among embarked slaves (WOMRAT1)",
		null=True,
		blank=True)

	percentage_boys_among_landed_slaves = models.FloatField(
		"Percentage of boys among landed slaves (BOYRAT3)",
		null=True,
		blank=True)

	child_ratio_among_landed_slaves = models.FloatField(
		"Child ratio among landed slaves (CHILRAT3)", null=True, blank=True)

	percentage_girls_among_landed_slaves = models.FloatField(
		"Percentage of girls among landed slaves (GIRLRAT3)",
		null=True,
		blank=True)

	male_ratio_among_landed_slaves = models.FloatField(
		"Male ratio among landed slaves (MALRAT3)", null=True, blank=True)

	percentage_men_among_landed_slaves = models.FloatField(
		"Percentage of men among landed slaves (MENRAT3)",
		null=True,
		blank=True)

	percentage_women_among_landed_slaves = models.FloatField(
		"Percentage of women among landed slaves (WOMRAT3)",
		null=True, blank=True)

	# INSERT HERE any new number variables [model]

	voyage = models.ForeignKey(
		'Voyage',
		related_name="voyage_name_slave_characteristics",
		on_delete=models.CASCADE)

	# menrat7
	percentage_men = models.FloatField("Percentage men on voyage (MENRAT7)",
									   null=True,
									   blank=True)
	# womrat7
	percentage_women = models.FloatField(
		"Percentage women on voyage (WOMRAT7)",
		null=True, blank=True)
	# boyrat7
	percentage_boy = models.FloatField("Percentage boy on voyage (BOYRAT7)",
									   null=True,
									   blank=True)
	# girlrat7
	percentage_girl = models.FloatField("Percentage girl on voyage (GIRLRAT7)",
										null=True,
										blank=True)
	# malrat7
	percentage_male = models.FloatField("Percentage male on voyage (MALRAT7)",
										null=True,
										blank=True)
	# chilrat7
	percentage_child = models.FloatField(
		"Percentage children on voyage (CHILRAT7)", null=True, blank=True)
	# Calculated from chilrat7
	percentage_adult = models.FloatField("Percentage adult on voyage",
										 null=True,
										 blank=True)
	# Calculated from malrat7
	percentage_female = models.FloatField("Percentage female on voyage",
										  null=True,
										  blank=True)

	# vymrtrat
	imp_mortality_ratio = models.FloatField(
		"Imputed mortality ratio (VYMRTRAT)", null=True, blank=True)

	class Meta:
		verbose_name = "Numbers of Voyage Captives"
		verbose_name_plural = "Numbers of Voyages' Captives"


class VoyageSourcesType(models.Model):
	"""
	Voyage sources type.
	Representing the group of sources.
	"""

	group_id = models.IntegerField()
	group_name = models.CharField(max_length=30)

	class Meta:
		verbose_name = "Sources type"
		verbose_name_plural = "Sources types"
		ordering = ['group_id']

	def __str__(self):
		return self.group_name


# TODO: Apply models.IntegerChoices when we migrate to Django 3+


class VoyageDataset:
	Transatlantic = 0
	IntraAmerican = 1
	IntraAfrican = 2


# Voyage Sources


class VoyageSources(models.Model):
	"""
	Voyage sources.
	Representing the original variables SOURCEA, SOURCEB, SOURCEC
	and etc to SOURCER
	"""

	short_ref = models.CharField('Short reference',
								 max_length=255, null=False, blank=True,
								 unique=True)
	# Might contain HTML text formatting
	full_ref = models.CharField('Full reference',
								max_length=2550, null=False, blank=True)
	source_type = models.ForeignKey('VoyageSourcesType', verbose_name="Source Type", null=False,
									on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Source"
		verbose_name_plural = "Sources"
		ordering = ['short_ref', 'full_ref']

	def __str__(self):
		return self.short_ref


class VoyageSourcesConnection(models.Model):
	"""
	Represents the relationship between Voyage and VoyageSources
	source_order determines the order sources appear for each voyage
	related to: :class:`~voyages.apps.voyage.models.VoyageSources`
	related to: :class:`~voyages.apps.voyage.models.Voyage`
	"""
	source = models.ForeignKey(	'VoyageSources',
							   	on_delete=models.CASCADE)
	voyage = models.ForeignKey(	'Voyage',
								related_name="voyage_sourceconnection",
							 	 on_delete=models.CASCADE)
	#source_order = models.IntegerField()
	text_ref = models.CharField('Text reference(citation)',
								max_length=255, null=False, blank=True)
	doc = models.ForeignKey( 	Doc,
								on_delete=models.CASCADE,null=True,blank=True)

class VoyageDatasetManager(models.Manager):

	def __init__(self, dataset):
		self.dataset = int(dataset)
		super().__init__()

	def get_queryset(self):
		return Voyage.all_dataset_objects.filter(dataset=self.dataset)


class LinkedVoyages(models.Model):
	"""
	Allow pairs of voyages to be linked.
	"""
	first = models.ForeignKey('Voyage', related_name="links_to_other_voyages",
							  on_delete=models.CASCADE)
	second = models.ForeignKey('Voyage', related_name="+",
							   on_delete=models.CASCADE)
	mode = models.IntegerField()

	# In this mode the first voyage is the IntraAmerican voyage
	# and the second is a transatlantic voyage.
	INTRA_AMERICAN_LINK_MODE = 1

class Voyage(models.Model):
	"""
	Information about voyages.
	related to: :class:`~voyages.apps.voyage.models.VoyageGroupings`
	related to: :class:`~voyages.apps.voyage.models.VoyageCaptain`
	related to: :class:`~voyages.apps.voyage.models.VoyageShipOwner`
	related to: :class:`~voyages.apps.voyage.models.VoyageSources`
	#new naming convention (mar 17) -- reverse lookups will have 'reverse' name format
	##e.g., the reverse link/related name to the captain table from the voyage table is now "voyage_captain" ... 
	## and the related name to the voyage table from the ship table is "ship_voyage"
	#new m2m rule -- avoiding the m2m "through" convention where there's data on the intermediate/"through" table
	###(which is all of them as of now)
	##formerly "through" tables will instead point at their connecting tables
	##lookups can then be performed using the new reverse lookup naming convention as above
	##also, finally (mostly) fixed the outcome tables' foreign key to outcomes just like with dates or itinerary
	"""

	voyage_id = models.IntegerField("Voyage ID", unique=True)

	voyage_in_cd_rom = models.BooleanField("Voyage in 1999 CD-ROM?",
										   max_length=1,
										   default=False,
										   blank=True)

	# Technical variables
	voyage_groupings = models.ForeignKey(	'VoyageGroupings',
											verbose_name="Voyage Groupings",
											related_name='groupings_voyage',
											blank=True,
											null=True,
											on_delete=models.CASCADE)

	# Data and imputed variables
	voyage_ship = models.ForeignKey(	'VoyageShip',
										verbose_name="Ship",
										related_name='ship_voyage',
										blank=True,
										null=True,
										on_delete=models.CASCADE)
	voyage_itinerary = models.ForeignKey(	'VoyageItinerary',
											verbose_name="Itinerary",
											related_name='itinerary_voyage',
											blank=True,
											null=True,
											on_delete=models.CASCADE)
	voyage_dates = models.ForeignKey(	'VoyageDates',
										verbose_name="Dates",
										related_name='dates_voyage',
										blank=True,
										null=True,
										on_delete=models.CASCADE)
	voyage_crew = models.ForeignKey('VoyageCrew',
									verbose_name="Crew",
									related_name='crew_voyage',
									blank=True,
									null=True,
									on_delete=models.CASCADE)
	voyage_slaves_numbers = models.ForeignKey(
		'VoyageSlavesNumbers',
		related_name='slaves_numbers_voyage',
		blank=True,
		null=True,
		on_delete=models.CASCADE)
	
	voyage_outcome = models.ForeignKey(
		'VoyageOutcome',
		related_name='outcome_voyage',
		blank=True,
		null=True,
		on_delete=models.CASCADE)
		
	last_update = models.DateTimeField(auto_now=True)
	
	african_info = models.ManyToManyField(AfricanInfo, related_name='african_info', blank=True)
	
	cargo = models.ManyToManyField(CargoType, through='VoyageCargoConnection', blank=True)
	
	dataset = models.IntegerField(
		null=False,
		default=VoyageDataset.Transatlantic,
		help_text='Which dataset the voyage belongs to '
				  '(e.g. Transatlantic, IntraAmerican)'
	)
	
	# generate natural key
	def natural_key(self):
		return (self.voyage_id,)

	def save(self, *args, **kwargs):
		if self.pk is None:
			self.pk = self.voyage_id
		super().save(*args, **kwargs)

	class Admin:
		manager = models.Manager()

	class Meta:
		ordering = [
			'voyage_id',
		]
		verbose_name = "Voyage"
		verbose_name_plural = "Voyages"

	def __str__(self):
		return "Voyage #%s" % str(self.voyage_id)


