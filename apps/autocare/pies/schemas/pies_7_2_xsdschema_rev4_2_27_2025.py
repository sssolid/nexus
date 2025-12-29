from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from xsdata.models.datatype import XmlDate

__NAMESPACE__ = "http://www.autocare.org"


@dataclass
class Pies:
    """
    Document Root Element.

    :ivar header: (Ref# A01)
    :ivar price_sheets: Parent Element Supporting PriceSheet Iterations
    :ivar marketing_copy: Parent Element Supporting Non-Item Specific
        Market Copy
    :ivar items: Parent Element Supporting Item Iterations
    :ivar trailer: (Ref# Z01)
    """

    class Meta:
        name = "PIES"
        namespace = "http://www.autocare.org"

    header: Optional["Pies.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
            "required": True,
        },
    )
    price_sheets: Optional["Pies.PriceSheets"] = field(
        default=None,
        metadata={
            "name": "PriceSheets",
            "type": "Element",
        },
    )
    marketing_copy: Optional["Pies.MarketingCopy"] = field(
        default=None,
        metadata={
            "name": "MarketingCopy",
            "type": "Element",
        },
    )
    items: Optional["Pies.Items"] = field(
        default=None,
        metadata={
            "name": "Items",
            "type": "Element",
            "required": True,
        },
    )
    trailer: Optional["Pies.Trailer"] = field(
        default=None,
        metadata={
            "name": "Trailer",
            "type": "Element",
            "required": True,
        },
    )

    @dataclass
    class Header:
        """
        :ivar piesversion: (Ref# A02)
        :ivar submission_type: (Ref# A03)
        :ivar blanket_effective_date: (Ref# A05)
        :ivar changes_since_date: (Ref# A06)
        :ivar parent_dunsnumber: (Ref# A10)
        :ivar parent_gln: (Ref# A11)
        :ivar parent_vmrsid: (Ref# A12)
        :ivar parent_aaiaid: (Ref# A13)
        :ivar brand_owner_duns: (Ref# A20)
        :ivar brand_owner_gln: (Ref# A21)
        :ivar brand_owner_vmrsid: (Ref# A22)
        :ivar buyer_duns: (Ref# A30)
        :ivar currency_code: (Ref# A35)
        :ivar language_code: (Ref A37)
        :ivar technical_contact: (Ref# A40)
        :ivar contact_email: (Ref# A41)
        :ivar pcdb_version_date: (Ref# A42)
        :ivar padb_version_date: (Ref# A43)
        """

        piesversion: Optional[str] = field(
            default=None,
            metadata={
                "name": "PIESVersion",
                "type": "Element",
                "required": True,
                "min_length": 3,
                "max_length": 5,
            },
        )
        submission_type: Optional[str] = field(
            default=None,
            metadata={
                "name": "SubmissionType",
                "type": "Element",
                "required": True,
                "min_length": 4,
                "max_length": 6,
            },
        )
        blanket_effective_date: Optional[XmlDate] = field(
            default=None,
            metadata={
                "name": "BlanketEffectiveDate",
                "type": "Element",
            },
        )
        changes_since_date: Optional[XmlDate] = field(
            default=None,
            metadata={
                "name": "ChangesSinceDate",
                "type": "Element",
            },
        )
        parent_dunsnumber: Optional[str] = field(
            default=None,
            metadata={
                "name": "ParentDUNSNumber",
                "type": "Element",
                "min_length": 9,
                "max_length": 13,
            },
        )
        parent_gln: Optional[str] = field(
            default=None,
            metadata={
                "name": "ParentGLN",
                "type": "Element",
                "length": 13,
            },
        )
        parent_vmrsid: Optional[str] = field(
            default=None,
            metadata={
                "name": "ParentVMRSID",
                "type": "Element",
                "length": 5,
            },
        )
        parent_aaiaid: Optional[str] = field(
            default=None,
            metadata={
                "name": "ParentAAIAID",
                "type": "Element",
                "length": 4,
            },
        )
        brand_owner_duns: Optional[str] = field(
            default=None,
            metadata={
                "name": "BrandOwnerDUNS",
                "type": "Element",
                "min_length": 9,
                "max_length": 13,
            },
        )
        brand_owner_gln: Optional[str] = field(
            default=None,
            metadata={
                "name": "BrandOwnerGLN",
                "type": "Element",
                "length": 13,
            },
        )
        brand_owner_vmrsid: Optional[str] = field(
            default=None,
            metadata={
                "name": "BrandOwnerVMRSID",
                "type": "Element",
                "length": 5,
            },
        )
        buyer_duns: Optional[str] = field(
            default=None,
            metadata={
                "name": "BuyerDuns",
                "type": "Element",
                "min_length": 9,
                "max_length": 13,
            },
        )
        currency_code: Optional[str] = field(
            default=None,
            metadata={
                "name": "CurrencyCode",
                "type": "Element",
                "length": 3,
            },
        )
        language_code: Optional[str] = field(
            default=None,
            metadata={
                "name": "LanguageCode",
                "type": "Element",
                "length": 2,
            },
        )
        technical_contact: Optional[str] = field(
            default=None,
            metadata={
                "name": "TechnicalContact",
                "type": "Element",
                "min_length": 1,
                "max_length": 60,
            },
        )
        contact_email: Optional[str] = field(
            default=None,
            metadata={
                "name": "ContactEmail",
                "type": "Element",
                "min_length": 1,
                "max_length": 254,
            },
        )
        pcdb_version_date: Optional[XmlDate] = field(
            default=None,
            metadata={
                "name": "PCdbVersionDate",
                "type": "Element",
                "required": True,
            },
        )
        padb_version_date: Optional[XmlDate] = field(
            default=None,
            metadata={
                "name": "PAdbVersionDate",
                "type": "Element",
            },
        )

    @dataclass
    class PriceSheets:
        """
        :ivar price_sheet: (Ref# A50)
        """

        price_sheet: list["Pies.PriceSheets.PriceSheet"] = field(
            default_factory=list,
            metadata={
                "name": "PriceSheet",
                "type": "Element",
                "min_occurs": 1,
            },
        )

        @dataclass
        class PriceSheet:
            """
            :ivar price_sheet_number: (Ref# A52)
            :ivar price_sheet_name: (Ref# A53)
            :ivar superseded_price_sheet_number: (Ref# A55)
            :ivar currency_code: (Ref# A60)
            :ivar price_zone: (Ref# A65)
            :ivar effective_date: (Ref# A70)
            :ivar expiration_date: (Ref# A75)
            :ivar maintenance_type: (Ref# A51)
            """

            price_sheet_number: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PriceSheetNumber",
                    "type": "Element",
                    "required": True,
                    "min_length": 1,
                    "max_length": 15,
                },
            )
            price_sheet_name: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PriceSheetName",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 30,
                },
            )
            superseded_price_sheet_number: Optional[str] = field(
                default=None,
                metadata={
                    "name": "SupersededPriceSheetNumber",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 15,
                },
            )
            currency_code: Optional[str] = field(
                default=None,
                metadata={
                    "name": "CurrencyCode",
                    "type": "Element",
                    "length": 3,
                },
            )
            price_zone: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PriceZone",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 10,
                    "pattern": r"[\p{L}]+",
                },
            )
            effective_date: Optional[XmlDate] = field(
                default=None,
                metadata={
                    "name": "EffectiveDate",
                    "type": "Element",
                },
            )
            expiration_date: Optional[XmlDate] = field(
                default=None,
                metadata={
                    "name": "ExpirationDate",
                    "type": "Element",
                },
            )
            maintenance_type: Optional[str] = field(
                default=None,
                metadata={
                    "name": "MaintenanceType",
                    "type": "Attribute",
                    "required": True,
                    "length": 1,
                },
            )

    @dataclass
    class MarketingCopy:
        """
        :ivar market_copy: (Ref# A80)
        """

        market_copy: list["Pies.MarketingCopy.MarketCopy"] = field(
            default_factory=list,
            metadata={
                "name": "MarketCopy",
                "type": "Element",
                "min_occurs": 1,
            },
        )

        @dataclass
        class MarketCopy:
            """
            :ivar market_copy_content: (Ref# A87)
            :ivar digital_assets: Parent Element Supporting
                DigitalFileInformation Iterations
            """

            market_copy_content: Optional[
                "Pies.MarketingCopy.MarketCopy.MarketCopyContent"
            ] = field(
                default=None,
                metadata={
                    "name": "MarketCopyContent",
                    "type": "Element",
                    "required": True,
                },
            )
            digital_assets: Optional[
                "Pies.MarketingCopy.MarketCopy.DigitalAssets"
            ] = field(
                default=None,
                metadata={
                    "name": "DigitalAssets",
                    "type": "Element",
                },
            )

            @dataclass
            class MarketCopyContent:
                """
                :ivar value:
                :ivar maintenance_type: (Ref# A81)
                :ivar market_copy_code: (Ref# A82)
                :ivar market_copy_reference: (Ref# A83)
                :ivar market_copy_sub_code: (Ref# A84)
                :ivar market_copy_sub_code_reference: (Ref# A85)
                :ivar market_copy_type: (Ref# A86)
                :ivar record_sequence: (Ref# A88)
                :ivar language_code: (Ref# A89)
                """

                value: str = field(
                    default="",
                    metadata={
                        "required": True,
                        "min_length": 1,
                        "max_length": 2000,
                    },
                )
                maintenance_type: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "MaintenanceType",
                        "type": "Attribute",
                        "required": True,
                        "length": 1,
                    },
                )
                market_copy_code: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "MarketCopyCode",
                        "type": "Attribute",
                        "required": True,
                        "length": 3,
                    },
                )
                market_copy_reference: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "MarketCopyReference",
                        "type": "Attribute",
                        "required": True,
                        "max_length": 240,
                    },
                )
                market_copy_sub_code: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "MarketCopySubCode",
                        "type": "Attribute",
                        "length": 3,
                    },
                )
                market_copy_sub_code_reference: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "MarketCopySubCodeReference",
                        "type": "Attribute",
                        "min_length": 1,
                        "max_length": 240,
                    },
                )
                market_copy_type: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "MarketCopyType",
                        "type": "Attribute",
                        "required": True,
                        "length": 3,
                    },
                )
                record_sequence: Optional[int] = field(
                    default=None,
                    metadata={
                        "name": "RecordSequence",
                        "type": "Attribute",
                        "min_inclusive": 1,
                        "max_inclusive": 99999,
                    },
                )
                language_code: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "LanguageCode",
                        "type": "Attribute",
                        "length": 2,
                    },
                )

            @dataclass
            class DigitalAssets:
                """
                :ivar digital_file_information: (Ref# M01)
                """

                digital_file_information: list[
                    "Pies.MarketingCopy.MarketCopy.DigitalAssets.DigitalFileInformation"
                ] = field(
                    default_factory=list,
                    metadata={
                        "name": "DigitalFileInformation",
                        "type": "Element",
                        "min_occurs": 1,
                    },
                )

                @dataclass
                class DigitalFileInformation:
                    """
                    :ivar file_name: (Ref# M05)
                    :ivar asset_type: (Ref# M10)
                    :ivar file_type: (Ref# M15)
                    :ivar representation: (Ref# M20)
                    :ivar file_size: (Ref# M25)
                    :ivar resolution: (Ref# M30)
                    :ivar color_mode: (Ref# M35)
                    :ivar background: (Ref# M40)
                    :ivar orientation_view: (Ref# M45)
                    :ivar asset_dimensions: Parent Element for Asset
                        Measurement Child Elements
                    :ivar file_path: (Ref# M75)
                    :ivar uri: (Ref# M80)
                    :ivar duration: (Ref# M81, M82)
                    :ivar frame: (Ref# M83)
                    :ivar total_frames: (Ref# M84)
                    :ivar plane: (Ref# M85)
                    :ivar hemisphere: (Ref# M86)
                    :ivar plunge: (Ref# M87)
                    :ivar total_planes: (Ref# M88)
                    :ivar asset_descriptions: (Ref# M64)
                    :ivar asset_dates: (Ref# M93)
                    :ivar country: (Ref# M98)
                    :ivar maintenance_type: (Ref# M02)
                    :ivar asset_id: (Ref# M06)
                    :ivar language_code: (Ref# M99)
                    """

                    file_name: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "FileName",
                            "type": "Element",
                            "required": True,
                            "min_length": 1,
                            "max_length": 80,
                        },
                    )
                    asset_type: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "AssetType",
                            "type": "Element",
                            "required": True,
                            "length": 3,
                        },
                    )
                    file_type: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "FileType",
                            "type": "Element",
                            "min_length": 3,
                            "max_length": 4,
                        },
                    )
                    representation: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "Representation",
                            "type": "Element",
                            "length": 1,
                        },
                    )
                    file_size: Optional[int] = field(
                        default=None,
                        metadata={
                            "name": "FileSize",
                            "type": "Element",
                            "total_digits": 10,
                        },
                    )
                    resolution: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "Resolution",
                            "type": "Element",
                            "min_length": 2,
                            "max_length": 4,
                        },
                    )
                    color_mode: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "ColorMode",
                            "type": "Element",
                            "length": 3,
                        },
                    )
                    background: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "Background",
                            "type": "Element",
                            "length": 3,
                        },
                    )
                    orientation_view: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "OrientationView",
                            "type": "Element",
                            "length": 3,
                        },
                    )
                    asset_dimensions: Optional[
                        "Pies.MarketingCopy.MarketCopy.DigitalAssets.DigitalFileInformation.AssetDimensions"
                    ] = field(
                        default=None,
                        metadata={
                            "name": "AssetDimensions",
                            "type": "Element",
                        },
                    )
                    file_path: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "FilePath",
                            "type": "Element",
                            "min_length": 1,
                            "max_length": 80,
                        },
                    )
                    uri: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "URI",
                            "type": "Element",
                            "max_length": 2000,
                        },
                    )
                    duration: Optional[
                        "Pies.MarketingCopy.MarketCopy.DigitalAssets.DigitalFileInformation.Duration"
                    ] = field(
                        default=None,
                        metadata={
                            "name": "Duration",
                            "type": "Element",
                        },
                    )
                    frame: Optional[int] = field(
                        default=None,
                        metadata={
                            "name": "Frame",
                            "type": "Element",
                            "total_digits": 3,
                        },
                    )
                    total_frames: Optional[int] = field(
                        default=None,
                        metadata={
                            "name": "TotalFrames",
                            "type": "Element",
                            "total_digits": 3,
                        },
                    )
                    plane: Optional[int] = field(
                        default=None,
                        metadata={
                            "name": "Plane",
                            "type": "Element",
                            "total_digits": 3,
                        },
                    )
                    hemisphere: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "Hemisphere",
                            "type": "Element",
                            "length": 1,
                        },
                    )
                    plunge: Optional[Decimal] = field(
                        default=None,
                        metadata={
                            "name": "Plunge",
                            "type": "Element",
                            "min_exclusive": Decimal("0"),
                            "total_digits": 6,
                        },
                    )
                    total_planes: Optional[int] = field(
                        default=None,
                        metadata={
                            "name": "TotalPlanes",
                            "type": "Element",
                        },
                    )
                    asset_descriptions: Optional[
                        "Pies.MarketingCopy.MarketCopy.DigitalAssets.DigitalFileInformation.AssetDescriptions"
                    ] = field(
                        default=None,
                        metadata={
                            "name": "AssetDescriptions",
                            "type": "Element",
                        },
                    )
                    asset_dates: Optional[
                        "Pies.MarketingCopy.MarketCopy.DigitalAssets.DigitalFileInformation.AssetDates"
                    ] = field(
                        default=None,
                        metadata={
                            "name": "AssetDates",
                            "type": "Element",
                        },
                    )
                    country: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "Country",
                            "type": "Element",
                            "length": 2,
                        },
                    )
                    maintenance_type: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "MaintenanceType",
                            "type": "Attribute",
                            "required": True,
                            "length": 1,
                        },
                    )
                    asset_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "AssetID",
                            "type": "Attribute",
                            "min_length": 1,
                            "max_length": 34,
                        },
                    )
                    language_code: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "LanguageCode",
                            "type": "Attribute",
                            "length": 2,
                        },
                    )

                    @dataclass
                    class AssetDimensions:
                        """
                        :ivar asset_height: (Ref# M50)
                        :ivar asset_width: (Ref# M55)
                        :ivar uom: (Ref# M60)
                        """

                        asset_height: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "AssetHeight",
                                "type": "Element",
                                "min_exclusive": Decimal("0"),
                                "total_digits": 6,
                                "fraction_digits": 4,
                            },
                        )
                        asset_width: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "AssetWidth",
                                "type": "Element",
                                "min_exclusive": Decimal("0"),
                                "total_digits": 6,
                                "fraction_digits": 4,
                            },
                        )
                        uom: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "UOM",
                                "type": "Attribute",
                                "required": True,
                                "length": 2,
                            },
                        )

                    @dataclass
                    class Duration:
                        value: Optional[int] = field(
                            default=None,
                            metadata={
                                "required": True,
                                "total_digits": 3,
                            },
                        )
                        uom: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "UOM",
                                "type": "Attribute",
                                "required": True,
                                "length": 2,
                            },
                        )

                    @dataclass
                    class AssetDescriptions:
                        """
                        :ivar description: (Ref# M71, M72, M73, M74)
                        """

                        description: list[
                            "Pies.MarketingCopy.MarketCopy.DigitalAssets.DigitalFileInformation.AssetDescriptions.Description"
                        ] = field(
                            default_factory=list,
                            metadata={
                                "name": "Description",
                                "type": "Element",
                                "min_occurs": 1,
                            },
                        )

                        @dataclass
                        class Description:
                            value: str = field(
                                default="",
                                metadata={
                                    "required": True,
                                    "min_length": 1,
                                    "max_length": 2000,
                                },
                            )
                            maintenance_type: Optional[str] = field(
                                default=None,
                                metadata={
                                    "name": "MaintenanceType",
                                    "type": "Attribute",
                                    "required": True,
                                    "length": 1,
                                },
                            )
                            description_code: Optional[str] = field(
                                default=None,
                                metadata={
                                    "name": "DescriptionCode",
                                    "type": "Attribute",
                                    "required": True,
                                    "length": 3,
                                },
                            )
                            language_code: Optional[str] = field(
                                default=None,
                                metadata={
                                    "name": "LanguageCode",
                                    "type": "Attribute",
                                    "length": 2,
                                },
                            )

                    @dataclass
                    class AssetDates:
                        """
                        :ivar asset_date: (Ref# M94, M95)
                        """

                        asset_date: list[
                            "Pies.MarketingCopy.MarketCopy.DigitalAssets.DigitalFileInformation.AssetDates.AssetDate"
                        ] = field(
                            default_factory=list,
                            metadata={
                                "name": "AssetDate",
                                "type": "Element",
                                "min_occurs": 1,
                            },
                        )

                        @dataclass
                        class AssetDate:
                            value: Optional[XmlDate] = field(
                                default=None,
                                metadata={
                                    "required": True,
                                },
                            )
                            asset_date_type: Optional[str] = field(
                                default=None,
                                metadata={
                                    "name": "assetDateType",
                                    "type": "Attribute",
                                    "length": 3,
                                },
                            )

    @dataclass
    class Items:
        """
        :ivar item: (Ref# B01)
        """

        item: list["Pies.Items.Item"] = field(
            default_factory=list,
            metadata={
                "name": "Item",
                "type": "Element",
                "min_occurs": 1,
            },
        )

        @dataclass
        class Item:
            """
            :ivar hazardous_material_code: (Ref# B03)
            :ivar base_item_id: (Ref# B05)
            :ivar item_level_gtin: (Ref# B10)
            :ivar part_number: (Ref# B15)
            :ivar brand_aaiaid: (Ref# B20)
            :ivar brand_label: (Ref# B25)
            :ivar sub_brand_aaiaid: (Ref# B27)
            :ivar sub_brand_label: (Ref# B28)
            :ivar vmrsbrand_id: (Ref# B29)
            :ivar acesapplications: (Ref# B30)
            :ivar item_quantity_size: (Ref# B32)
            :ivar container_type: (Ref# B34)
            :ivar quantity_per_application: (Ref# B40)
            :ivar item_effective_date: (Ref# B45)
            :ivar available_date: (Ref# B50)
            :ivar minimum_order_quantity: (Ref# B55)
            :ivar manufacturer_product_codes: Parent Element for Product
                Code Child Elements (Ref# B59)
            :ivar aaiaproduct_category_code: (Ref# B62)
            :ivar unspsc: (Ref# B63)
            :ivar part_terminology_id: (Ref# B64)
            :ivar vmrscode: (Ref# B65)
            :ivar descriptions: Parent Element Supporting Description
                (Ref# C01)
            :ivar prices: Parent Element Supporting Price Iterations
            :ivar extended_information: Parent Element Supporting
                ExtendedProductInformation Iterations (Ref# E01)
            :ivar product_attributes: Parent Element Supporting
                ProductAttribute Iterations (Ref# F01)
            :ivar packages: Parent Element Supporting Package Iterations
            :ivar kits: Parent Element Supporting Kit Iterations (Ref#
                K01)
            :ivar part_interchange_info: Parent Element Supporting
                PartInterchange Iterations
            :ivar digital_assets: Parent Element Supporting
                DigitalFileInformation Iterations
            :ivar maintenance_type: (Ref# B02)
            """

            hazardous_material_code: Optional[str] = field(
                default=None,
                metadata={
                    "name": "HazardousMaterialCode",
                    "type": "Element",
                    "length": 1,
                },
            )
            base_item_id: Optional[str] = field(
                default=None,
                metadata={
                    "name": "BaseItemID",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 48,
                },
            )
            item_level_gtin: Optional["Pies.Items.Item.ItemLevelGtin"] = field(
                default=None,
                metadata={
                    "name": "ItemLevelGTIN",
                    "type": "Element",
                },
            )
            part_number: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PartNumber",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 48,
                },
            )
            brand_aaiaid: Optional[str] = field(
                default=None,
                metadata={
                    "name": "BrandAAIAID",
                    "type": "Element",
                    "length": 4,
                },
            )
            brand_label: Optional[str] = field(
                default=None,
                metadata={
                    "name": "BrandLabel",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 60,
                },
            )
            sub_brand_aaiaid: Optional[str] = field(
                default=None,
                metadata={
                    "name": "SubBrandAAIAID",
                    "type": "Element",
                    "length": 4,
                },
            )
            sub_brand_label: Optional[str] = field(
                default=None,
                metadata={
                    "name": "SubBrandLabel",
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 60,
                },
            )
            vmrsbrand_id: Optional[str] = field(
                default=None,
                metadata={
                    "name": "VMRSBrandID",
                    "type": "Element",
                    "length": 5,
                },
            )
            acesapplications: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACESApplications",
                    "type": "Element",
                    "length": 1,
                },
            )
            item_quantity_size: Optional[
                "Pies.Items.Item.ItemQuantitySize"
            ] = field(
                default=None,
                metadata={
                    "name": "ItemQuantitySize",
                    "type": "Element",
                },
            )
            container_type: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ContainerType",
                    "type": "Element",
                    "length": 2,
                },
            )
            quantity_per_application: Optional[
                "Pies.Items.Item.QuantityPerApplication"
            ] = field(
                default=None,
                metadata={
                    "name": "QuantityPerApplication",
                    "type": "Element",
                },
            )
            item_effective_date: Optional[XmlDate] = field(
                default=None,
                metadata={
                    "name": "ItemEffectiveDate",
                    "type": "Element",
                },
            )
            available_date: Optional[XmlDate] = field(
                default=None,
                metadata={
                    "name": "AvailableDate",
                    "type": "Element",
                },
            )
            minimum_order_quantity: Optional[
                "Pies.Items.Item.MinimumOrderQuantity"
            ] = field(
                default=None,
                metadata={
                    "name": "MinimumOrderQuantity",
                    "type": "Element",
                },
            )
            manufacturer_product_codes: Optional[
                "Pies.Items.Item.ManufacturerProductCodes"
            ] = field(
                default=None,
                metadata={
                    "name": "ManufacturerProductCodes",
                    "type": "Element",
                },
            )
            aaiaproduct_category_code: Optional[str] = field(
                default=None,
                metadata={
                    "name": "AAIAProductCategoryCode",
                    "type": "Element",
                    "length": 6,
                },
            )
            unspsc: Optional[str] = field(
                default=None,
                metadata={
                    "name": "UNSPSC",
                    "type": "Element",
                    "min_length": 8,
                    "max_length": 10,
                },
            )
            part_terminology_id: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PartTerminologyID",
                    "type": "Element",
                    "min_length": 4,
                    "max_length": 5,
                },
            )
            vmrscode: Optional[str] = field(
                default=None,
                metadata={
                    "name": "VMRSCode",
                    "type": "Element",
                    "length": 9,
                },
            )
            descriptions: Optional["Pies.Items.Item.Descriptions"] = field(
                default=None,
                metadata={
                    "name": "Descriptions",
                    "type": "Element",
                },
            )
            prices: Optional["Pies.Items.Item.Prices"] = field(
                default=None,
                metadata={
                    "name": "Prices",
                    "type": "Element",
                },
            )
            extended_information: Optional[
                "Pies.Items.Item.ExtendedInformation"
            ] = field(
                default=None,
                metadata={
                    "name": "ExtendedInformation",
                    "type": "Element",
                },
            )
            product_attributes: Optional[
                "Pies.Items.Item.ProductAttributes"
            ] = field(
                default=None,
                metadata={
                    "name": "ProductAttributes",
                    "type": "Element",
                },
            )
            packages: Optional["Pies.Items.Item.Packages"] = field(
                default=None,
                metadata={
                    "name": "Packages",
                    "type": "Element",
                },
            )
            kits: Optional["Pies.Items.Item.Kits"] = field(
                default=None,
                metadata={
                    "name": "Kits",
                    "type": "Element",
                },
            )
            part_interchange_info: Optional[
                "Pies.Items.Item.PartInterchangeInfo"
            ] = field(
                default=None,
                metadata={
                    "name": "PartInterchangeInfo",
                    "type": "Element",
                },
            )
            digital_assets: Optional["Pies.Items.Item.DigitalAssets"] = field(
                default=None,
                metadata={
                    "name": "DigitalAssets",
                    "type": "Element",
                },
            )
            maintenance_type: Optional[str] = field(
                default=None,
                metadata={
                    "name": "MaintenanceType",
                    "type": "Attribute",
                    "required": True,
                    "length": 1,
                },
            )

            @dataclass
            class ItemLevelGtin:
                """
                :ivar value:
                :ivar gtinqualifier: (Ref# B11)
                """

                value: str = field(
                    default="",
                    metadata={
                        "required": True,
                        "length": 14,
                    },
                )
                gtinqualifier: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "GTINQualifier",
                        "type": "Attribute",
                        "required": True,
                        "length": 2,
                    },
                )

            @dataclass
            class ItemQuantitySize:
                """
                :ivar value:
                :ivar uom: (Ref# B33)
                """

                value: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "required": True,
                        "min_exclusive": Decimal("0"),
                        "total_digits": 8,
                    },
                )
                uom: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "UOM",
                        "type": "Attribute",
                        "length": 2,
                    },
                )

            @dataclass
            class QuantityPerApplication:
                """
                :ivar value:
                :ivar qualifier: (Ref# B35)
                :ivar uom: (Ref# B41)
                """

                value: str = field(
                    default="",
                    metadata={
                        "required": True,
                    },
                )
                qualifier: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "Qualifier",
                        "type": "Attribute",
                        "length": 3,
                    },
                )
                uom: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "UOM",
                        "type": "Attribute",
                        "required": True,
                        "length": 2,
                    },
                )

            @dataclass
            class MinimumOrderQuantity:
                """
                :ivar value:
                :ivar uom: (Ref# B56)
                """

                value: Optional[int] = field(
                    default=None,
                    metadata={
                        "required": True,
                        "max_inclusive": 99999999,
                    },
                )
                uom: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "UOM",
                        "type": "Attribute",
                        "required": True,
                        "length": 2,
                    },
                )

            @dataclass
            class ManufacturerProductCodes:
                """
                :ivar group: (Ref# B60)
                :ivar sub_group: (Ref# B61)
                """

                group: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "Group",
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 10,
                    },
                )
                sub_group: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "SubGroup",
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 10,
                    },
                )

            @dataclass
            class Descriptions:
                """
                :ivar description: (Ref# C10)
                """

                description: list[
                    "Pies.Items.Item.Descriptions.Description"
                ] = field(
                    default_factory=list,
                    metadata={
                        "name": "Description",
                        "type": "Element",
                        "min_occurs": 1,
                    },
                )

                @dataclass
                class Description:
                    """
                    :ivar value:
                    :ivar maintenance_type: (Ref# C02)
                    :ivar description_code: (Ref# C05)
                    :ivar language_code: (Ref# C15)
                    :ivar sequence: (Ref# C16)
                    """

                    value: str = field(
                        default="",
                        metadata={
                            "required": True,
                            "min_length": 1,
                            "max_length": 2000,
                        },
                    )
                    maintenance_type: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "MaintenanceType",
                            "type": "Attribute",
                            "required": True,
                            "length": 1,
                        },
                    )
                    description_code: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "DescriptionCode",
                            "type": "Attribute",
                            "required": True,
                            "length": 3,
                        },
                    )
                    language_code: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "LanguageCode",
                            "type": "Attribute",
                            "length": 2,
                        },
                    )
                    sequence: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "Sequence",
                            "type": "Attribute",
                        },
                    )

            @dataclass
            class Prices:
                """
                :ivar pricing: (Ref# D01)
                """

                pricing: list["Pies.Items.Item.Prices.Pricing"] = field(
                    default_factory=list,
                    metadata={
                        "name": "Pricing",
                        "type": "Element",
                        "min_occurs": 1,
                    },
                )

                @dataclass
                class Pricing:
                    """
                    :ivar price_sheet_number: (Ref# D05)
                    :ivar currency_code: (Ref# D15)
                    :ivar effective_date: (Ref# D25)
                    :ivar expiration_date: (Ref# D30)
                    :ivar price: (Ref# D40)
                    :ivar price_type_description: (Ref# D36)
                    :ivar price_break: (Ref# D45)
                    :ivar price_multiplier: (Ref# D42)
                    :ivar maintenance_type: (Ref# D02)
                    :ivar price_type: (Ref# D35)
                    """

                    price_sheet_number: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "PriceSheetNumber",
                            "type": "Element",
                            "required": True,
                            "min_length": 1,
                            "max_length": 15,
                        },
                    )
                    currency_code: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "CurrencyCode",
                            "type": "Element",
                            "length": 3,
                        },
                    )
                    effective_date: Optional[XmlDate] = field(
                        default=None,
                        metadata={
                            "name": "EffectiveDate",
                            "type": "Element",
                        },
                    )
                    expiration_date: Optional[XmlDate] = field(
                        default=None,
                        metadata={
                            "name": "ExpirationDate",
                            "type": "Element",
                        },
                    )
                    price: Optional["Pies.Items.Item.Prices.Pricing.Price"] = (
                        field(
                            default=None,
                            metadata={
                                "name": "Price",
                                "type": "Element",
                                "required": True,
                            },
                        )
                    )
                    price_type_description: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "PriceTypeDescription",
                            "type": "Element",
                            "min_length": 1,
                            "max_length": 80,
                        },
                    )
                    price_break: Optional[
                        "Pies.Items.Item.Prices.Pricing.PriceBreak"
                    ] = field(
                        default=None,
                        metadata={
                            "name": "PriceBreak",
                            "type": "Element",
                        },
                    )
                    price_multiplier: Optional[Decimal] = field(
                        default=None,
                        metadata={
                            "name": "PriceMultiplier",
                            "type": "Element",
                            "total_digits": 10,
                            "fraction_digits": 4,
                        },
                    )
                    maintenance_type: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "MaintenanceType",
                            "type": "Attribute",
                            "required": True,
                            "length": 1,
                        },
                    )
                    price_type: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "PriceType",
                            "type": "Attribute",
                            "required": True,
                            "length": 3,
                        },
                    )

                    @dataclass
                    class Price:
                        """
                        :ivar value:
                        :ivar uom: (Ref# D41)
                        """

                        value: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "required": True,
                                "min_exclusive": Decimal("0"),
                                "total_digits": 10,
                                "fraction_digits": 4,
                            },
                        )
                        uom: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "UOM",
                                "type": "Attribute",
                                "required": True,
                                "length": 2,
                            },
                        )

                    @dataclass
                    class PriceBreak:
                        """
                        :ivar value:
                        :ivar uom: (Ref# D46)
                        """

                        value: Optional[int] = field(
                            default=None,
                            metadata={
                                "required": True,
                                "max_inclusive": 99999999,
                            },
                        )
                        uom: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "UOM",
                                "type": "Attribute",
                                "required": True,
                                "length": 2,
                            },
                        )

            @dataclass
            class ExtendedInformation:
                """
                :ivar extended_product_information: (Ref# E10)
                """

                extended_product_information: list[
                    "Pies.Items.Item.ExtendedInformation.ExtendedProductInformation"
                ] = field(
                    default_factory=list,
                    metadata={
                        "name": "ExtendedProductInformation",
                        "type": "Element",
                        "min_occurs": 1,
                    },
                )

                @dataclass
                class ExtendedProductInformation:
                    """
                    :ivar value:
                    :ivar maintenance_type: (Ref# E02)
                    :ivar expicode: (Ref# E05)
                    :ivar language_code: (Ref# E15)
                    """

                    value: str = field(
                        default="",
                        metadata={
                            "required": True,
                            "min_length": 1,
                            "max_length": 2000,
                        },
                    )
                    maintenance_type: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "MaintenanceType",
                            "type": "Attribute",
                            "required": True,
                            "length": 1,
                        },
                    )
                    expicode: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "EXPICode",
                            "type": "Attribute",
                            "required": True,
                            "length": 3,
                        },
                    )
                    language_code: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "LanguageCode",
                            "type": "Attribute",
                            "length": 2,
                        },
                    )

            @dataclass
            class ProductAttributes:
                """
                :ivar product_attribute: (Ref# F10)
                """

                product_attribute: list[
                    "Pies.Items.Item.ProductAttributes.ProductAttribute"
                ] = field(
                    default_factory=list,
                    metadata={
                        "name": "ProductAttribute",
                        "type": "Element",
                        "min_occurs": 1,
                    },
                )

                @dataclass
                class ProductAttribute:
                    """
                    :ivar value:
                    :ivar maintenance_type: (Ref# F02)
                    :ivar attribute_id: (Ref# F05)
                    :ivar padbattribute: (Ref# F07)
                    :ivar attribute_uom: (Ref# F08)
                    :ivar style_id: (Ref# F11)
                    :ivar record_number: (Ref# F15)
                    :ivar multi_value_quantity: (Ref# F17)
                    :ivar multi_value_sequence: (Ref# F18)
                    :ivar language_code: (Ref# F20)
                    """

                    value: str = field(
                        default="",
                        metadata={
                            "required": True,
                            "min_length": 1,
                            "max_length": 2000,
                        },
                    )
                    maintenance_type: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "MaintenanceType",
                            "type": "Attribute",
                            "required": True,
                            "length": 1,
                        },
                    )
                    attribute_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "AttributeID",
                            "type": "Attribute",
                            "required": True,
                            "min_length": 1,
                            "max_length": 80,
                        },
                    )
                    padbattribute: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "PADBAttribute",
                            "type": "Attribute",
                            "required": True,
                            "length": 1,
                        },
                    )
                    attribute_uom: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "AttributeUOM",
                            "type": "Attribute",
                            "min_length": 1,
                            "max_length": 20,
                        },
                    )
                    style_id: Optional[int] = field(
                        default=None,
                        metadata={
                            "name": "StyleID",
                            "type": "Attribute",
                            "min_inclusive": 1,
                            "max_inclusive": 99999,
                        },
                    )
                    record_number: Optional[int] = field(
                        default=None,
                        metadata={
                            "name": "RecordNumber",
                            "type": "Attribute",
                            "min_inclusive": 1,
                            "max_inclusive": 999,
                        },
                    )
                    multi_value_quantity: Optional[int] = field(
                        default=None,
                        metadata={
                            "name": "MultiValueQuantity",
                            "type": "Attribute",
                            "min_inclusive": 1,
                            "max_inclusive": 999,
                        },
                    )
                    multi_value_sequence: Optional[int] = field(
                        default=None,
                        metadata={
                            "name": "MultiValueSequence",
                            "type": "Attribute",
                            "min_inclusive": 1,
                            "max_inclusive": 999,
                        },
                    )
                    language_code: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "LanguageCode",
                            "type": "Attribute",
                            "length": 2,
                        },
                    )

            @dataclass
            class Packages:
                """
                :ivar package: (Ref# H01)
                """

                package: list["Pies.Items.Item.Packages.Package"] = field(
                    default_factory=list,
                    metadata={
                        "name": "Package",
                        "type": "Element",
                        "min_occurs": 1,
                    },
                )

                @dataclass
                class Package:
                    """
                    :ivar package_level_gtin: (Ref# H05)
                    :ivar electronic_product_code: (Ref# H07)
                    :ivar package_bar_code_characters: (Ref# H10)
                    :ivar package_uom: (Ref# H15)
                    :ivar quantityof_eaches: (Ref# H20)
                    :ivar inner_quantity: (Ref# H21)
                    :ivar orderable: (Ref# H24)
                    :ivar dimensions: Parent Element Containing
                        Dimensional Child Elements (Ref# H39)
                    :ivar weights: Parent Element Containing Weight
                        Child Elements (Ref# H44)
                    :ivar weight_variance: (Ref# H47)
                    :ivar stacking_factor: (Ref# H55)
                    :ivar hazardous_material: (Ref# J01)
                    :ivar maintenance_type: (Ref# H02)
                    """

                    package_level_gtin: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "PackageLevelGTIN",
                            "type": "Element",
                            "length": 14,
                        },
                    )
                    electronic_product_code: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "ElectronicProductCode",
                            "type": "Element",
                            "length": 27,
                        },
                    )
                    package_bar_code_characters: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "PackageBarCodeCharacters",
                            "type": "Element",
                            "min_length": 1,
                            "max_length": 48,
                        },
                    )
                    package_uom: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "PackageUOM",
                            "type": "Element",
                            "required": True,
                            "length": 2,
                        },
                    )
                    quantityof_eaches: Optional[int] = field(
                        default=None,
                        metadata={
                            "name": "QuantityofEaches",
                            "type": "Element",
                            "required": True,
                            "min_inclusive": 1,
                            "max_inclusive": 99999999,
                        },
                    )
                    inner_quantity: Optional[
                        "Pies.Items.Item.Packages.Package.InnerQuantity"
                    ] = field(
                        default=None,
                        metadata={
                            "name": "InnerQuantity",
                            "type": "Element",
                        },
                    )
                    orderable: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "Orderable",
                            "type": "Element",
                            "length": 1,
                        },
                    )
                    dimensions: Optional[
                        "Pies.Items.Item.Packages.Package.Dimensions"
                    ] = field(
                        default=None,
                        metadata={
                            "name": "Dimensions",
                            "type": "Element",
                        },
                    )
                    weights: Optional[
                        "Pies.Items.Item.Packages.Package.Weights"
                    ] = field(
                        default=None,
                        metadata={
                            "name": "Weights",
                            "type": "Element",
                        },
                    )
                    weight_variance: Optional[Decimal] = field(
                        default=None,
                        metadata={
                            "name": "WeightVariance",
                            "type": "Element",
                            "min_exclusive": Decimal("0"),
                            "total_digits": 8,
                            "fraction_digits": 4,
                        },
                    )
                    stacking_factor: Optional[int] = field(
                        default=None,
                        metadata={
                            "name": "StackingFactor",
                            "type": "Element",
                            "min_inclusive": 1,
                            "total_digits": 3,
                        },
                    )
                    hazardous_material: list[
                        "Pies.Items.Item.Packages.Package.HazardousMaterial"
                    ] = field(
                        default_factory=list,
                        metadata={
                            "name": "HazardousMaterial",
                            "type": "Element",
                        },
                    )
                    maintenance_type: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "MaintenanceType",
                            "type": "Attribute",
                            "required": True,
                            "length": 1,
                        },
                    )

                    @dataclass
                    class InnerQuantity:
                        """
                        :ivar value:
                        :ivar inner_quantity_uom: (Ref# H22)
                        """

                        value: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "required": True,
                                "min_exclusive": Decimal("0"),
                                "total_digits": 8,
                            },
                        )
                        inner_quantity_uom: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "InnerQuantityUOM",
                                "type": "Attribute",
                                "required": True,
                                "length": 2,
                            },
                        )

                    @dataclass
                    class Dimensions:
                        """
                        :ivar merchandising_height: (Ref# H25)
                        :ivar merchandising_width: (Ref H30)
                        :ivar merchandising_length: (Ref# H35)
                        :ivar shipping_height: (Ref# H36)
                        :ivar shipping_width: (Ref# H37)
                        :ivar shipping_length: (Ref# H38)
                        :ivar uom: (Ref# H40)
                        """

                        merchandising_height: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "MerchandisingHeight",
                                "type": "Element",
                                "required": True,
                                "min_exclusive": Decimal("0"),
                                "total_digits": 8,
                                "fraction_digits": 4,
                            },
                        )
                        merchandising_width: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "MerchandisingWidth",
                                "type": "Element",
                                "required": True,
                                "min_exclusive": Decimal("0"),
                                "total_digits": 8,
                                "fraction_digits": 4,
                            },
                        )
                        merchandising_length: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "MerchandisingLength",
                                "type": "Element",
                                "required": True,
                                "min_exclusive": Decimal("0"),
                                "total_digits": 8,
                                "fraction_digits": 4,
                            },
                        )
                        shipping_height: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "ShippingHeight",
                                "type": "Element",
                                "required": True,
                                "min_exclusive": Decimal("0"),
                                "total_digits": 8,
                                "fraction_digits": 4,
                            },
                        )
                        shipping_width: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "ShippingWidth",
                                "type": "Element",
                                "required": True,
                                "min_exclusive": Decimal("0"),
                                "total_digits": 8,
                                "fraction_digits": 4,
                            },
                        )
                        shipping_length: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "ShippingLength",
                                "type": "Element",
                                "required": True,
                                "min_exclusive": Decimal("0"),
                                "total_digits": 8,
                                "fraction_digits": 4,
                            },
                        )
                        uom: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "UOM",
                                "type": "Attribute",
                                "required": True,
                                "length": 2,
                            },
                        )

                    @dataclass
                    class Weights:
                        """
                        :ivar weight: (Ref# H45)
                        :ivar dimensional_weight: (Ref# H50)
                        :ivar uom: (Ref# H46)
                        """

                        weight: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "Weight",
                                "type": "Element",
                                "required": True,
                                "min_exclusive": Decimal("0"),
                                "total_digits": 9,
                                "fraction_digits": 4,
                            },
                        )
                        dimensional_weight: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "DimensionalWeight",
                                "type": "Element",
                                "min_exclusive": Decimal("0"),
                                "total_digits": 9,
                                "fraction_digits": 4,
                            },
                        )
                        uom: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "UOM",
                                "type": "Attribute",
                                "required": True,
                                "length": 2,
                            },
                        )

                    @dataclass
                    class HazardousMaterial:
                        """
                        :ivar shipping_scope: (Ref# J04)
                        :ivar bulk: (Ref# J05)
                        :ivar regulating_country: (Ref# J10)
                        :ivar transport_method: (Ref# J15)
                        :ivar regulated: (Ref# J20)
                        :ivar description: (Ref# J25)
                        :ivar hazardous_material_code_qualifier: (Ref#
                            J31)
                        :ivar hazardous_material_description: (Ref# J33)
                        :ivar hazardous_material_label_code: (Ref# J34)
                        :ivar shipping_name: (Ref# J35)
                        :ivar unnaidcode: (Ref# J40)
                        :ivar hazardous_placard_notation: (Ref# J45)
                        :ivar whmiscode: (Ref# J46)
                        :ivar whmisfree_text: (Ref# J47)
                        :ivar packing_group_code: (Ref# J50)
                        :ivar regulations_exemption_code: (Ref# J55)
                        :ivar text_message: (Ref# J60)
                        :ivar outer_package_label: (Ref# J65)
                        :ivar maintenance_type: (Ref# J02)
                        :ivar language_code: (Ref# J70)
                        """

                        shipping_scope: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "ShippingScope",
                                "type": "Element",
                                "required": True,
                                "length": 3,
                            },
                        )
                        bulk: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "Bulk",
                                "type": "Element",
                                "required": True,
                                "length": 1,
                            },
                        )
                        regulating_country: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "RegulatingCountry",
                                "type": "Element",
                                "required": True,
                                "length": 2,
                            },
                        )
                        transport_method: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "TransportMethod",
                                "type": "Element",
                                "required": True,
                                "length": 1,
                            },
                        )
                        regulated: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "Regulated",
                                "type": "Element",
                                "required": True,
                                "length": 1,
                            },
                        )
                        description: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "Description",
                                "type": "Element",
                                "min_length": 1,
                                "max_length": 200,
                            },
                        )
                        hazardous_material_code_qualifier: Optional[str] = (
                            field(
                                default=None,
                                metadata={
                                    "name": "HazardousMaterialCodeQualifier",
                                    "type": "Element",
                                    "length": 1,
                                },
                            )
                        )
                        hazardous_material_description: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "HazardousMaterialDescription",
                                "type": "Element",
                                "min_length": 1,
                                "max_length": 80,
                            },
                        )
                        hazardous_material_label_code: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "HazardousMaterialLabelCode",
                                "type": "Element",
                                "min_length": 1,
                                "max_length": 4,
                            },
                        )
                        shipping_name: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "ShippingName",
                                "type": "Element",
                                "min_length": 1,
                                "max_length": 260,
                            },
                        )
                        unnaidcode: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "UNNAIDCode",
                                "type": "Element",
                                "length": 6,
                            },
                        )
                        hazardous_placard_notation: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "HazardousPlacardNotation",
                                "type": "Element",
                                "min_length": 1,
                                "max_length": 40,
                            },
                        )
                        whmiscode: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "WHMISCode",
                                "type": "Element",
                                "min_length": 1,
                                "max_length": 10,
                            },
                        )
                        whmisfree_text: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "WHMISFreeText",
                                "type": "Element",
                                "min_length": 1,
                                "max_length": 80,
                            },
                        )
                        packing_group_code: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "PackingGroupCode",
                                "type": "Element",
                                "min_length": 1,
                                "max_length": 3,
                            },
                        )
                        regulations_exemption_code: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "RegulationsExemptionCode",
                                "type": "Element",
                                "min_length": 1,
                                "max_length": 4,
                            },
                        )
                        text_message: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "TextMessage",
                                "type": "Element",
                                "min_length": 1,
                                "max_length": 2000,
                            },
                        )
                        outer_package_label: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "OuterPackageLabel",
                                "type": "Element",
                                "min_length": 1,
                                "max_length": 20,
                            },
                        )
                        maintenance_type: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "MaintenanceType",
                                "type": "Attribute",
                                "required": True,
                                "length": 1,
                            },
                        )
                        language_code: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "LanguageCode",
                                "type": "Attribute",
                                "length": 2,
                            },
                        )

            @dataclass
            class Kits:
                """
                :ivar kit_component: (Ref# K35)
                """

                kit_component: list["Pies.Items.Item.Kits.KitComponent"] = (
                    field(
                        default_factory=list,
                        metadata={
                            "name": "KitComponent",
                            "type": "Element",
                            "min_occurs": 1,
                        },
                    )
                )

                @dataclass
                class KitComponent:
                    """
                    :ivar component_part_number: (Ref# K03)
                    :ivar component_brand: (Ref# K04)
                    :ivar component_brand_label: (Ref# K05)
                    :ivar component_sub_brand: (Ref# K06)
                    :ivar component_sub_brand_label: (Ref# K07)
                    :ivar description: (Ref# K10)
                    :ivar component_part_terminology_id: (Ref# K11)
                    :ivar quantity_in_kit: (Ref# K15)
                    :ivar sequence_code: (Ref# K30)
                    :ivar sold_separately: (Ref# K31)
                    :ivar maintenance_type: (Ref# K02)
                    """

                    component_part_number: Optional[
                        "Pies.Items.Item.Kits.KitComponent.ComponentPartNumber"
                    ] = field(
                        default=None,
                        metadata={
                            "name": "ComponentPartNumber",
                            "type": "Element",
                        },
                    )
                    component_brand: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "ComponentBrand",
                            "type": "Element",
                            "length": 4,
                        },
                    )
                    component_brand_label: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "ComponentBrandLabel",
                            "type": "Element",
                            "min_length": 1,
                            "max_length": 60,
                        },
                    )
                    component_sub_brand: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "ComponentSubBrand",
                            "type": "Element",
                            "length": 4,
                        },
                    )
                    component_sub_brand_label: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "ComponentSubBrandLabel",
                            "type": "Element",
                            "min_length": 1,
                            "max_length": 60,
                        },
                    )
                    description: Optional[
                        "Pies.Items.Item.Kits.KitComponent.Description"
                    ] = field(
                        default=None,
                        metadata={
                            "name": "Description",
                            "type": "Element",
                            "required": True,
                        },
                    )
                    component_part_terminology_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "ComponentPartTerminologyID",
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 8,
                        },
                    )
                    quantity_in_kit: Optional[
                        "Pies.Items.Item.Kits.KitComponent.QuantityInKit"
                    ] = field(
                        default=None,
                        metadata={
                            "name": "QuantityInKit",
                            "type": "Element",
                            "required": True,
                        },
                    )
                    sequence_code: Optional[int] = field(
                        default=None,
                        metadata={
                            "name": "SequenceCode",
                            "type": "Element",
                            "min_inclusive": 1,
                            "max_inclusive": 999,
                        },
                    )
                    sold_separately: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "SoldSeparately",
                            "type": "Element",
                            "required": True,
                        },
                    )
                    maintenance_type: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "MaintenanceType",
                            "type": "Attribute",
                            "required": True,
                            "length": 1,
                        },
                    )

                    @dataclass
                    class ComponentPartNumber:
                        """
                        :ivar value:
                        :ivar idqualifier: (Ref# K08)
                        """

                        value: str = field(
                            default="",
                            metadata={
                                "required": True,
                                "min_length": 1,
                                "max_length": 48,
                            },
                        )
                        idqualifier: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "IDQualifier",
                                "type": "Attribute",
                                "length": 2,
                            },
                        )

                    @dataclass
                    class Description:
                        """
                        :ivar value:
                        :ivar description_code: (Ref# K09)
                        :ivar language_code: (Ref# K12)
                        """

                        value: str = field(
                            default="",
                            metadata={
                                "required": True,
                                "min_length": 1,
                                "max_length": 2000,
                            },
                        )
                        description_code: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "DescriptionCode",
                                "type": "Attribute",
                                "required": True,
                                "length": 3,
                            },
                        )
                        language_code: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "LanguageCode",
                                "type": "Attribute",
                                "length": 2,
                            },
                        )

                    @dataclass
                    class QuantityInKit:
                        """
                        :ivar value:
                        :ivar uom: (Ref# K20)
                        """

                        value: Optional[int] = field(
                            default=None,
                            metadata={
                                "required": True,
                                "max_inclusive": 99999999,
                            },
                        )
                        uom: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "UOM",
                                "type": "Attribute",
                                "required": True,
                                "length": 2,
                            },
                        )

            @dataclass
            class PartInterchangeInfo:
                """
                :ivar part_interchange: (Ref# N01)
                """

                part_interchange: list[
                    "Pies.Items.Item.PartInterchangeInfo.PartInterchange"
                ] = field(
                    default_factory=list,
                    metadata={
                        "name": "PartInterchange",
                        "type": "Element",
                        "min_occurs": 1,
                    },
                )

                @dataclass
                class PartInterchange:
                    """
                    :ivar part_number: (Ref# N20)
                    :ivar maintenance_type: (Ref# N02)
                    :ivar brand_aaiaid: (Ref# N10)
                    :ivar brand_label: (Ref# N11)
                    :ivar sub_brand_aaiaid: (Ref# N12)
                    :ivar sub_brand_label: (Ref# N13)
                    :ivar vmrsbrand_id: (Ref# N14)
                    :ivar item_equivalent_uom: (Ref# N16)
                    :ivar quality_grade_level: (Ref# N25)
                    :ivar internal_notes: (Ref# N35)
                    :ivar language_code: (Ref# N40)
                    """

                    part_number: list[
                        "Pies.Items.Item.PartInterchangeInfo.PartInterchange.PartNumber"
                    ] = field(
                        default_factory=list,
                        metadata={
                            "name": "PartNumber",
                            "type": "Element",
                            "min_occurs": 1,
                        },
                    )
                    maintenance_type: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "MaintenanceType",
                            "type": "Attribute",
                            "required": True,
                            "length": 1,
                        },
                    )
                    brand_aaiaid: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "BrandAAIAID",
                            "type": "Attribute",
                            "length": 4,
                        },
                    )
                    brand_label: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "BrandLabel",
                            "type": "Attribute",
                            "min_length": 1,
                            "max_length": 60,
                        },
                    )
                    sub_brand_aaiaid: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "SubBrandAAIAID",
                            "type": "Attribute",
                            "length": 4,
                        },
                    )
                    sub_brand_label: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "SubBrandLabel",
                            "type": "Attribute",
                            "min_length": 1,
                            "max_length": 60,
                        },
                    )
                    vmrsbrand_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "VMRSBrandID",
                            "type": "Attribute",
                            "length": 5,
                        },
                    )
                    item_equivalent_uom: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "ItemEquivalentUOM",
                            "type": "Attribute",
                            "length": 2,
                        },
                    )
                    quality_grade_level: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "QualityGradeLevel",
                            "type": "Attribute",
                            "length": 1,
                        },
                    )
                    internal_notes: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "InternalNotes",
                            "type": "Attribute",
                            "min_length": 1,
                            "max_length": 240,
                        },
                    )
                    language_code: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "LanguageCode",
                            "type": "Attribute",
                            "length": 2,
                        },
                    )

                    @dataclass
                    class PartNumber:
                        """
                        :ivar value:
                        :ivar reference_item: (Ref# N21)
                        :ivar interchange_quantity: (Ref# N26)
                        :ivar uom: (Ref# N27)
                        :ivar interchange_notes: (Ref# N30)
                        """

                        value: str = field(
                            default="",
                            metadata={
                                "required": True,
                                "min_length": 1,
                                "max_length": 48,
                            },
                        )
                        reference_item: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "ReferenceItem",
                                "type": "Attribute",
                                "min_length": 1,
                                "max_length": 48,
                            },
                        )
                        interchange_quantity: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "InterchangeQuantity",
                                "type": "Attribute",
                                "min_exclusive": Decimal("0"),
                                "total_digits": 8,
                            },
                        )
                        uom: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "UOM",
                                "type": "Attribute",
                                "length": 2,
                            },
                        )
                        interchange_notes: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "InterchangeNotes",
                                "type": "Attribute",
                                "min_length": 1,
                                "max_length": 240,
                            },
                        )

            @dataclass
            class DigitalAssets:
                """
                :ivar digital_file_information: (Ref# P01)
                """

                digital_file_information: list[
                    "Pies.Items.Item.DigitalAssets.DigitalFileInformation"
                ] = field(
                    default_factory=list,
                    metadata={
                        "name": "DigitalFileInformation",
                        "type": "Element",
                        "min_occurs": 1,
                    },
                )

                @dataclass
                class DigitalFileInformation:
                    """
                    :ivar file_name: (Ref# P05)
                    :ivar asset_type: (Ref# P10)
                    :ivar file_type: (Ref# P15)
                    :ivar representation: (Ref# P20)
                    :ivar file_size: (Ref# P25)
                    :ivar resolution: (Ref# P30)
                    :ivar color_mode: (Ref# P35)
                    :ivar background: (Ref# P40)
                    :ivar orientation_view: (Ref# P45)
                    :ivar asset_dimensions: Parent Element for Asset
                        Measurement Child Elements
                    :ivar file_path: (Ref# P75)
                    :ivar uri: (Ref# P80)
                    :ivar duration: (Ref# P81, P82)
                    :ivar frame: (Ref# P83)
                    :ivar total_frames: (Ref# P84)
                    :ivar plane: (Ref# P85)
                    :ivar hemisphere: (Ref# P86)
                    :ivar plunge: (Ref# P87)
                    :ivar total_planes: (Ref# P88)
                    :ivar asset_descriptions: (Ref# P64)
                    :ivar asset_dates: (Ref# P93)
                    :ivar country: (Ref# P98)
                    :ivar maintenance_type: (Ref# P02)
                    :ivar asset_id: (Ref# P06)
                    :ivar language_code: (Ref# P99)
                    """

                    file_name: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "FileName",
                            "type": "Element",
                            "required": True,
                            "min_length": 1,
                            "max_length": 80,
                        },
                    )
                    asset_type: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "AssetType",
                            "type": "Element",
                            "required": True,
                            "length": 3,
                        },
                    )
                    file_type: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "FileType",
                            "type": "Element",
                            "min_length": 3,
                            "max_length": 4,
                        },
                    )
                    representation: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "Representation",
                            "type": "Element",
                            "length": 1,
                        },
                    )
                    file_size: Optional[int] = field(
                        default=None,
                        metadata={
                            "name": "FileSize",
                            "type": "Element",
                            "total_digits": 10,
                        },
                    )
                    resolution: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "Resolution",
                            "type": "Element",
                            "min_length": 2,
                            "max_length": 4,
                        },
                    )
                    color_mode: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "ColorMode",
                            "type": "Element",
                            "length": 3,
                        },
                    )
                    background: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "Background",
                            "type": "Element",
                            "length": 3,
                        },
                    )
                    orientation_view: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "OrientationView",
                            "type": "Element",
                            "length": 3,
                        },
                    )
                    asset_dimensions: Optional[
                        "Pies.Items.Item.DigitalAssets.DigitalFileInformation.AssetDimensions"
                    ] = field(
                        default=None,
                        metadata={
                            "name": "AssetDimensions",
                            "type": "Element",
                        },
                    )
                    file_path: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "FilePath",
                            "type": "Element",
                            "min_length": 1,
                            "max_length": 80,
                        },
                    )
                    uri: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "URI",
                            "type": "Element",
                            "max_length": 2000,
                        },
                    )
                    duration: Optional[
                        "Pies.Items.Item.DigitalAssets.DigitalFileInformation.Duration"
                    ] = field(
                        default=None,
                        metadata={
                            "name": "Duration",
                            "type": "Element",
                        },
                    )
                    frame: Optional[int] = field(
                        default=None,
                        metadata={
                            "name": "Frame",
                            "type": "Element",
                            "total_digits": 3,
                        },
                    )
                    total_frames: Optional[int] = field(
                        default=None,
                        metadata={
                            "name": "TotalFrames",
                            "type": "Element",
                            "total_digits": 3,
                        },
                    )
                    plane: Optional[int] = field(
                        default=None,
                        metadata={
                            "name": "Plane",
                            "type": "Element",
                            "total_digits": 3,
                        },
                    )
                    hemisphere: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "Hemisphere",
                            "type": "Element",
                            "length": 1,
                        },
                    )
                    plunge: Optional[Decimal] = field(
                        default=None,
                        metadata={
                            "name": "Plunge",
                            "type": "Element",
                            "min_exclusive": Decimal("0"),
                            "total_digits": 6,
                        },
                    )
                    total_planes: Optional[int] = field(
                        default=None,
                        metadata={
                            "name": "TotalPlanes",
                            "type": "Element",
                        },
                    )
                    asset_descriptions: Optional[
                        "Pies.Items.Item.DigitalAssets.DigitalFileInformation.AssetDescriptions"
                    ] = field(
                        default=None,
                        metadata={
                            "name": "AssetDescriptions",
                            "type": "Element",
                        },
                    )
                    asset_dates: Optional[
                        "Pies.Items.Item.DigitalAssets.DigitalFileInformation.AssetDates"
                    ] = field(
                        default=None,
                        metadata={
                            "name": "AssetDates",
                            "type": "Element",
                        },
                    )
                    country: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "Country",
                            "type": "Element",
                            "length": 2,
                        },
                    )
                    maintenance_type: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "MaintenanceType",
                            "type": "Attribute",
                            "required": True,
                            "length": 1,
                        },
                    )
                    asset_id: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "AssetID",
                            "type": "Attribute",
                            "min_length": 1,
                            "max_length": 34,
                        },
                    )
                    language_code: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "LanguageCode",
                            "type": "Attribute",
                            "length": 2,
                        },
                    )

                    @dataclass
                    class AssetDimensions:
                        """
                        :ivar asset_height: (Ref# P50)
                        :ivar asset_width: (Ref# P55)
                        :ivar uom: (Ref# P60)
                        """

                        asset_height: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "AssetHeight",
                                "type": "Element",
                                "min_exclusive": Decimal("0"),
                                "total_digits": 6,
                                "fraction_digits": 4,
                            },
                        )
                        asset_width: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "AssetWidth",
                                "type": "Element",
                                "min_exclusive": Decimal("0"),
                                "total_digits": 6,
                                "fraction_digits": 4,
                            },
                        )
                        uom: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "UOM",
                                "type": "Attribute",
                                "required": True,
                                "length": 2,
                            },
                        )

                    @dataclass
                    class Duration:
                        value: Optional[int] = field(
                            default=None,
                            metadata={
                                "required": True,
                                "total_digits": 3,
                            },
                        )
                        uom: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "UOM",
                                "type": "Attribute",
                                "required": True,
                                "length": 2,
                            },
                        )

                    @dataclass
                    class AssetDescriptions:
                        """
                        :ivar description: (Ref# P71, P72, P73, P74)
                        """

                        description: list[
                            "Pies.Items.Item.DigitalAssets.DigitalFileInformation.AssetDescriptions.Description"
                        ] = field(
                            default_factory=list,
                            metadata={
                                "name": "Description",
                                "type": "Element",
                                "min_occurs": 1,
                            },
                        )

                        @dataclass
                        class Description:
                            value: str = field(
                                default="",
                                metadata={
                                    "required": True,
                                    "min_length": 1,
                                    "max_length": 2000,
                                },
                            )
                            maintenance_type: Optional[str] = field(
                                default=None,
                                metadata={
                                    "name": "MaintenanceType",
                                    "type": "Attribute",
                                    "required": True,
                                    "length": 1,
                                },
                            )
                            description_code: Optional[str] = field(
                                default=None,
                                metadata={
                                    "name": "DescriptionCode",
                                    "type": "Attribute",
                                    "required": True,
                                    "length": 3,
                                },
                            )
                            language_code: Optional[str] = field(
                                default=None,
                                metadata={
                                    "name": "LanguageCode",
                                    "type": "Attribute",
                                    "length": 2,
                                },
                            )

                    @dataclass
                    class AssetDates:
                        """
                        :ivar asset_date: (Ref# P94. P95)
                        """

                        asset_date: list[
                            "Pies.Items.Item.DigitalAssets.DigitalFileInformation.AssetDates.AssetDate"
                        ] = field(
                            default_factory=list,
                            metadata={
                                "name": "AssetDate",
                                "type": "Element",
                                "min_occurs": 1,
                            },
                        )

                        @dataclass
                        class AssetDate:
                            value: Optional[XmlDate] = field(
                                default=None,
                                metadata={
                                    "required": True,
                                },
                            )
                            asset_date_type: Optional[str] = field(
                                default=None,
                                metadata={
                                    "name": "assetDateType",
                                    "type": "Attribute",
                                    "length": 3,
                                },
                            )

    @dataclass
    class Trailer:
        """
        :ivar item_count: (Ref# Z10)
        :ivar transaction_date: (Ref# Z15)
        """

        item_count: Optional[int] = field(
            default=None,
            metadata={
                "name": "ItemCount",
                "type": "Element",
                "min_inclusive": 1,
                "max_inclusive": 9999999,
            },
        )
        transaction_date: Optional[XmlDate] = field(
            default=None,
            metadata={
                "name": "TransactionDate",
                "type": "Element",
                "required": True,
            },
        )
