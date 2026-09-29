import os
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.text import slugify

from apps.core.models import StudioProfile, StudioMetric, Page, PageSection, TeamMember
from apps.interior.models import InteriorCategory, InteriorProject, InteriorSpecification, InteriorGalleryImage
from apps.modelmaking.models import ModelCategory, PhysicalModelProject, FabricationSpecification, ModelGalleryImage
from apps.panorama.models import PanoramicTour, PanoramicScene, Hotspot
from apps.blog.models import BlogCategory, Author, BlogPost

class Command(BaseCommand):
    help = "Seed initial data for ROHA Architectural Studio using real frontend photography"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding ROHA studio data with local photography..."))

        frontend_public = settings.BASE_DIR.parent / 'roha-interior' / 'public'
        uploads_dir = Path(settings.MEDIA_ROOT)

        def copy_media(source_relative: str, target_subfolder: str) -> str:
            """Copies an image from frontend public folder into backend uploads subfolder."""
            src_file = frontend_public / source_relative
            if not src_file.exists():
                return ""
            target_dir = uploads_dir / target_subfolder
            target_dir.mkdir(parents=True, exist_ok=True)
            target_file = target_dir / src_file.name
            try:
                shutil.copy2(src_file, target_file)
                return f"{target_subfolder}/{src_file.name}"
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Could not copy {src_file.name}: {e}"))
                return ""

        # 1. Studio Profile & Metrics
        profile, _ = StudioProfile.objects.get_or_create(
            id=1,
            defaults={
                "studio_name": "ROHA Interior and Architects",
                "tagline": "Precision Model Making & Curated Interior Architecture",
                "about_narrative": "We shape spaces that evoke emotion and elevate human experience. From bespoke residential sanctuaries to high-performance commercial headquarters, our work synthesizes light, materiality, and ergonomic precision.",
                "address": "Golagol, Haile Gebre Silase St, Addis Ababa, HANAN K Plaza, 8th floor",
                "email": "roha@gmail.com",
                "phone": "+251 911 00 00 00",
                "whatsapp": "+251 911 00 00 00",
                "twitter_url": "https://twitter.com",
                "instagram_url": "https://instagram.com",
                "linkedin_url": "https://linkedin.com",
            }
        )

        metrics_data = [
            ("12", "YRS", "Experience", 1),
            ("350", "+", "Curated Interiors", 2),
            ("500", "+", "Scale Models", 3),
            ("0.1", "mm", "Precision Tolerance", 4),
        ]
        for num, unit, label, order in metrics_data:
            StudioMetric.objects.update_or_create(
                label=label,
                defaults={"metric_number": num, "unit": unit, "order": order}
            )

        # 2. Pages & Sections (Page Builder)
        pages_data = [
            ("home", "Home — ROHA Architectural Studio", "Master craftsmanship in scale modeling and contemporary interior architecture."),
            ("interior", "Interior Architecture & Spatial Curation", "Bespoke residential, penthouse, hospitality, and workspace interiors."),
            ("model-making", "Precision Scale Architectural Model Making", "0.1mm tolerance architectural scale models using hybrid 3D printing and laser cutting."),
            ("about", "About ROHA Studio", "Design manifesto, leadership, and architectural metrics."),
            ("contact", "Consultation & Project Inquiry", "Contact our principal architects and model fabricators."),
            ("gallery", "360 Virtual Reality Tour Archive", "Immersive virtual reality architectural walkthroughs."),
        ]
        for slug, title, desc in pages_data:
            page, _ = Page.objects.get_or_create(
                slug=slug,
                defaults={"title": title, "meta_description": desc, "is_active": True}
            )
            PageSection.objects.update_or_create(
                page=page,
                section_key="hero",
                defaults={
                    "heading": title,
                    "subheading": "ROHA Precision & Craft",
                    "body_text": desc,
                    "cta_text": "Start a Project",
                    "cta_link": "/contactus",
                    "order": 1,
                    "is_active": True,
                }
            )

        # 3. Interior Categories & Projects
        interior_cats = ["Residential", "Commercial", "Hospitality", "Retail", "Penthouse"]
        cat_map = {}
        for cname in interior_cats:
            cat, _ = InteriorCategory.objects.get_or_create(name=cname)
            cat_map[cname] = cat

        sample_interiors = [
            {
                "id": 1,
                "title": "Minimalist Modern Residence",
                "category": cat_map["Residential"],
                "year": "2024",
                "location": "Addis Ababa, Ethiopia",
                "desc": "Serene open-plan residential interior with monolithic concrete, warm timber joinery, and biophilic light wells.",
                "area": "450 m²",
                "style": "Contemporary Minimalist",
                "cover": copy_media("tr/279A1756.JPG", "interior"),
                "gallery": ["tr/279A1757.JPG", "tr/279A1758.JPG", "tr/279A1759.JPG"],
            },
            {
                "id": 2,
                "title": "Executive Tech Headquarters",
                "category": cat_map["Commercial"],
                "year": "2023",
                "location": "Bole, Addis Ababa",
                "desc": "Acoustically tuned corporate interiors featuring modular breakout spaces, oak slat paneling, and indirect lighting.",
                "area": "2,800 m²",
                "style": "Corporate Modern",
                "cover": copy_media("tr/279A1760.JPG", "interior"),
                "gallery": ["tr/279A1761.JPG", "tr/279A1762.JPG"],
            },
            {
                "id": 3,
                "title": "Azure Boutique Hotel Suite",
                "category": cat_map["Hospitality"],
                "year": "2024",
                "location": "Bishoftu, Ethiopia",
                "desc": "Luxury hospitality interior with custom brass accents, terrazzo flooring, and floor-to-ceiling panoramic drapery.",
                "area": "120 m²",
                "style": "Modern Luxury",
                "cover": copy_media("tr/279A1768.JPG", "interior"),
                "gallery": ["tr/279A1769.JPG", "tr/279A1770.JPG"],
            },
            {
                "id": 4,
                "title": "Atelier Flagship Store",
                "category": cat_map["Retail"],
                "year": "2024",
                "location": "Addis Ababa, Ethiopia",
                "desc": "Sculptural retail interior featuring fluted plaster walls, floating cantilevered plinths, and museum-grade spotlighting.",
                "area": "340 m²",
                "style": "Avant-Garde Retail",
                "cover": copy_media("tr/279A1771.JPG", "interior"),
                "gallery": ["tr/279A1772.JPG", "tr/279A1773.JPG"],
            },
            {
                "id": 5,
                "title": "Skyline Sky Villa Penthouse",
                "category": cat_map["Penthouse"],
                "year": "2024",
                "location": "Addis Ababa, Ethiopia",
                "desc": "Double-height penthouse interior showcasing bookmatched Calacatta marble, integrated wine cellar, and private terrace lounge.",
                "area": "620 m²",
                "style": "High-End Luxury",
                "cover": copy_media("confrence1.png", "interior"),
                "gallery": ["tr/279A1756.JPG"],
            },
            {
                "id": 6,
                "title": "Artisan Culinary Club",
                "category": cat_map["Hospitality"],
                "year": "2023",
                "location": "Addis Ababa, Ethiopia",
                "desc": "Intimate dining club with charred cedar wood finishes, bespoke velvet banquettes, and deep atmospheric illumination.",
                "area": "480 m²",
                "style": "Bespoke Hospitality",
                "cover": copy_media("home1.png", "interior"),
                "gallery": ["1.jpg", "3.jpg"],
            },
            {
                "id": 7,
                "title": "Contemporary Villa Salon",
                "category": cat_map["Residential"],
                "year": "2024",
                "location": "Addis Ababa, Ethiopia",
                "desc": "Spacious salon with custom curved sofa arrangement, travertine fireplace mantel, and garden courtyard integration.",
                "area": "310 m²",
                "style": "Contemporary Villa",
                "cover": copy_media("ethio1.jpg", "interior"),
                "gallery": ["ethio 2.jpg"],
            },
            {
                "id": 8,
                "title": "Haute Horlogerie Showroom",
                "category": cat_map["Retail"],
                "year": "2023",
                "location": "Bole, Addis Ababa",
                "desc": "High-security luxury retail space combining smoked glass vitrines, brushed bronze fittings, and acoustic suede wall panels.",
                "area": "220 m²",
                "style": "Precision Luxury",
                "cover": copy_media("ethio 2.jpg", "interior"),
                "gallery": ["20240807_180203.jpg"],
            },
        ]

        for item in sample_interiors:
            proj, _ = InteriorProject.objects.update_or_create(
                title=item["title"],
                defaults={
                    "category": item["category"],
                    "year": item["year"],
                    "location": item["location"],
                    "description": item["desc"],
                    "subtitle": item.get("subtitle", "Transforming the Future of Contemporary Living"),
                    "video_url": "https://www.youtube.com/embed/_BZZkFzuLQs",
                    "cover_image": item["cover"],
                    "is_featured": True,
                }
            )
            InteriorSpecification.objects.update_or_create(
                project=proj,
                defaults={
                    "area": item["area"],
                    "style": item["style"],
                    "material_palette": "Smoked oak, raw travertine, brass joinery",
                    "lighting_design": "Indirect 2700K LED coves",
                    "architect": "ROHA Design Team",
                    "client": "Private Client",
                    "status": "Completed",
                }
            )
            # Gallery
            for idx, gimg in enumerate(item.get("gallery", [])):
                gpath = copy_media(gimg, "interior/gallery")
                if gpath:
                    InteriorGalleryImage.objects.update_or_create(
                        project=proj,
                        image=gpath,
                        defaults={
                            "order": idx,
                            "caption": f"{proj.title} Perspective {idx+1}",
                            "subtitle": f"{item['style']} Curation",
                        }
                    )

        # 4. Model Making Categories & Projects
        model_cats = ["Architecture", "Commercial", "Cultural", "Hospitality", "Educational", "Healthcare", "Mixed-Use"]
        mcat_map = {}
        for mname in model_cats:
            mcat, _ = ModelCategory.objects.get_or_create(name=mname)
            mcat_map[mname] = mcat

        sample_models = [
            {
                "title": "Modern Residential Complex Scale Model",
                "category": mcat_map["Architecture"],
                "scale": "1:50",
                "year": "2024",
                "desc": "High-detail architectural scale model showcasing residential massing, fenestration louvers, and interior floor sections.",
                "cover": copy_media("tr/279A1812.JPG", "modelmaking"),
                "gallery": ["tr/279A1813.JPG", "tr/279A1815.JPG"],
            },
            {
                "title": "Corporate Headquarters Scale Model",
                "category": mcat_map["Commercial"],
                "scale": "1:100",
                "year": "2023",
                "desc": "Laser-cut acrylic tower model with integrated 3000K warm floor illumination and CNC-milled topography base.",
                "cover": copy_media("tr/279A1816.JPG", "modelmaking"),
                "gallery": ["tr/279A1817.JPG", "tr/279A1818.JPG"],
            },
            {
                "title": "Cultural Arts Center Massing Model",
                "category": mcat_map["Cultural"],
                "scale": "1:200",
                "year": "2024",
                "desc": "Fluid organic geometric physical model using hybrid high-resolution SLA resin 3D printing and hand finishing.",
                "cover": copy_media("tr/4V0A0305.JPG", "modelmaking"),
                "gallery": ["tr/4V0A0306.JPG", "tr/4V0A0307.JPG"],
            },
            {
                "title": "Luxury Hotel Resort Physical Model",
                "category": mcat_map["Hospitality"],
                "scale": "1:250",
                "year": "2023",
                "desc": "Five-star resort model featuring contour-layered topography, miniature landscape features, and illuminated pools.",
                "cover": copy_media("tr/4V0A0308.JPG", "modelmaking"),
                "gallery": ["tr/4V0A0305.JPG"],
            },
            {
                "title": "Educational Campus Scale Model",
                "category": mcat_map["Educational"],
                "scale": "1:500",
                "year": "2024",
                "desc": "Comprehensive masterplan model with interchangeable pavilion massing and perimeter pedestrian canopies.",
                "cover": copy_media("1.jpg", "modelmaking"),
                "gallery": ["3.jpg"],
            },
            {
                "title": "Shopping Mall Complex Scale Study",
                "category": mcat_map["Commercial"],
                "scale": "1:150",
                "year": "2023",
                "desc": "Translucent frosted acrylic atrium with visible internal escalators and structural space-frame trusses.",
                "cover": copy_media("3.jpg", "modelmaking"),
                "gallery": ["1.jpg"],
            },
            {
                "title": "Healthcare Facility Physical Model",
                "category": mcat_map["Healthcare"],
                "scale": "1:100",
                "year": "2024",
                "desc": "Advanced medical center physical model with color-coded modular zoning and helipad lighting.",
                "cover": copy_media("20240807_180203.jpg", "modelmaking"),
                "gallery": ["tr/279A1812.JPG"],
            },
            {
                "title": "Mixed-Use Development Scale Model",
                "category": mcat_map["Mixed-Use"],
                "scale": "1:200",
                "year": "2023",
                "desc": "Dense urban block model highlighting transit hub integration, multi-level skybridges, and pocket parks.",
                "cover": copy_media("tr/279A1816.JPG", "modelmaking"),
                "gallery": ["tr/279A1813.JPG"],
            },
        ]

        for mitem in sample_models:
            mproj, _ = PhysicalModelProject.objects.update_or_create(
                title=mitem["title"],
                defaults={
                    "category": mitem["category"],
                    "scale_ratio": mitem["scale"],
                    "year": mitem["year"],
                    "precision_tolerance": "0.1mm",
                    "description": mitem["desc"],
                    "cover_image": mitem["cover"],
                    "is_featured": True,
                }
            )
            FabricationSpecification.objects.update_or_create(
                project=mproj,
                defaults={
                    "scale": mitem["scale"],
                    "tolerance": "0.1mm precision",
                    "base_material": "Laser-cut acrylic, basswood, SLA resin",
                    "finish": "Satin architectural white, clear lacquered timber",
                    "lead_time": "3 weeks",
                    "client": "Urban Development Corp",
                    "status": "Completed",
                }
            )
            for idx, mgimg in enumerate(mitem.get("gallery", [])):
                mgpath = copy_media(mgimg, "modelmaking/gallery")
                if mgpath:
                    ModelGalleryImage.objects.get_or_create(
                        project=mproj,
                        image=mgpath,
                        defaults={"order": idx, "caption": f"{mproj.title} Scale Detail {idx+1}"}
                    )

        # 5. 360 Panorama Tours & Equirectangular Scenes
        tour1, _ = PanoramicTour.objects.update_or_create(
            id=1,
            defaults={
                "title": "Modern Residential Complex 360 Virtual Tour",
                "description": "Interactive virtual reality walkthrough of the flagship residential suite.",
                "cover_image": copy_media("tr/279A1756.JPG", "panoramas"),
                "is_featured": True,
            }
        )
        scene1, _ = PanoramicScene.objects.update_or_create(
            tour=tour1,
            scene_id="livingRoom",
            defaults={
                "name": "Living Room",
                "panorama": copy_media("tr/279A1002.JPG", "panoramas/equirectangular"),
                "initial_yaw": 0.0,
                "initial_pitch": 0.0,
                "order": 1
            }
        )
        scene2, _ = PanoramicScene.objects.update_or_create(
            tour=tour1,
            scene_id="kitchen",
            defaults={
                "name": "Kitchen",
                "panorama": copy_media("tr/279A1003.JPG", "panoramas/equirectangular"),
                "initial_yaw": 180.0,
                "initial_pitch": 0.0,
                "order": 2
            }
        )
        Hotspot.objects.update_or_create(
            scene=scene1,
            text="Go to Kitchen",
            defaults={
                "pitch": 10.0,
                "yaw": 150.0,
                "hotspot_type": "scene",
                "target_scene": scene2,
                "target_yaw": 0.0,
                "target_pitch": 0.0,
                "css_class": "custom-hotspot",
            }
        )
        Hotspot.objects.update_or_create(
            scene=scene2,
            text="Back to Living Room",
            defaults={
                "pitch": 5.0,
                "yaw": -170.0,
                "hotspot_type": "scene",
                "target_scene": scene1,
                "target_yaw": 150.0,
                "target_pitch": 10.0,
                "css_class": "custom-hotspot",
            }
        )

        tour2, _ = PanoramicTour.objects.update_or_create(
            id=2,
            defaults={
                "title": "Corporate Headquarters 360 Tour",
                "description": "High-resolution panoramic inspection of the executive atrium.",
                "cover_image": copy_media("tr/279A1760.JPG", "panoramas"),
                "is_featured": True,
            }
        )
        scene2_1, _ = PanoramicScene.objects.update_or_create(
            tour=tour2,
            scene_id="lobby",
            defaults={
                "name": "Main Lobby",
                "panorama": copy_media("tr/279A1763.JPG", "panoramas/equirectangular"),
                "initial_yaw": 0.0,
                "initial_pitch": 0.0,
                "order": 1
            }
        )

        # 6. Blog Categories & Posts with Local Visuals
        bcat_design, _ = BlogCategory.objects.get_or_create(name="Design")
        bcat_tech, _ = BlogCategory.objects.get_or_create(name="Technology")
        bcat_craft, _ = BlogCategory.objects.get_or_create(name="Craft & Fabrication")
        author, _ = Author.objects.get_or_create(name="Jennifer Taylor", defaults={"bio": "Senior Architectural Editor"})

        sample_posts = [
            {
                "title": "Minimalism in Modern Architectural & Spatial Design",
                "category": bcat_design,
                "type": "Opinion",
                "year": "2024",
                "read_time": "6 min read",
                "cover": copy_media("pexels-chudin-alexey-26964541.jpg", "blog"),
                "description": "Why restraint, pure materiality, and volumetric clarity are the foundations of contemporary luxury.",
                "content": [
                    {"type": "paragraph", "text": "In contemporary interior architecture, minimalism is not the absence of energy, but the presence of deliberate space."},
                    {"type": "heading", "text": "Material Authenticity"},
                    {"type": "paragraph", "text": "By paring away ornamental clutter, the inherent textures of oak, cast concrete, and hand-cut stone command focus."},
                    {"type": "list", "items": ["Restraint in palette", "Honesty of structural materials", "Light as an architectural element"]}
                ],
            },
            {
                "title": "Revolutionizing Spatial Planning Through Precision Scale Modeling",
                "category": bcat_craft,
                "type": "Case Study",
                "year": "2024",
                "read_time": "8 min read",
                "cover": copy_media("pexels-mikhail-peace-939247406-27120592.jpg", "blog"),
                "description": "How 0.1mm tolerance physical prototypes illuminate spatial dilemmas that CAD software cannot reveal.",
                "content": [
                    {"type": "paragraph", "text": "Physical architectural models provide an irreplaceable tactile understanding of proportion, ambient shadow fall, and material rhythm."},
                    {"type": "heading", "text": "Hybrid Digital & Hand Craft"},
                    {"type": "paragraph", "text": "We combine micro-SLA resin 3D printing with precision Japanese hand joinery to deliver presentation models that captivate clients."}
                ],
            },
            {
                "title": "Biophilic Light Wells and Volumetric Clarity",
                "category": bcat_design,
                "type": "Guide",
                "year": "2024",
                "read_time": "5 min read",
                "cover": copy_media("1.jpg", "blog"),
                "description": "Harnessing natural zenithal illumination to transform private living spaces into serene sanctuaries.",
                "content": [
                    {"type": "paragraph", "text": "Light from above carries a unique psychological calm. In our Addis Ababa residences, biophilic light wells act as living temporal art."}
                ],
            },
            {
                "title": "Material Authenticity in Luxury Hospitality Fit-Outs",
                "category": bcat_craft,
                "type": "Analysis",
                "year": "2023",
                "read_time": "7 min read",
                "cover": copy_media("3.jpg", "blog"),
                "description": "A deep dive into acoustic suede, travertine fireplace mantels, and custom brass joinery in high-traffic hotels.",
                "content": [
                    {"type": "paragraph", "text": "Hospitality environments demand both exquisite tactile luxury and resilient engineering."}
                ],
            },
            {
                "title": "Hybrid 3D Printing and Laser Cutting in Architectural Prototyping",
                "category": bcat_tech,
                "type": "Technology",
                "year": "2024",
                "read_time": "6 min read",
                "cover": copy_media("ethio1.jpg", "blog"),
                "description": "Balancing the speed of CNC additive fabrication with the warmth of American basswood.",
                "content": [
                    {"type": "paragraph", "text": "Modern scale model fabrication is an orchestra of precision digital machinery and artisanal patience."}
                ],
            },
            {
                "title": "The Dialogue Between Void and Form in Contemporary Residences",
                "category": bcat_design,
                "type": "Opinion",
                "year": "2024",
                "read_time": "9 min read",
                "cover": copy_media("ethio 2.jpg", "blog"),
                "description": "How deliberate negative space invites contemplation and elevates every day living.",
                "content": [
                    {"type": "paragraph", "text": "The greatest luxury in modern architecture is the confidence to leave room to breathe."}
                ],
            },
        ]

        for pdata in sample_posts:
            BlogPost.objects.update_or_create(
                title=pdata["title"],
                defaults={
                    "category": pdata["category"],
                    "author": author,
                    "article_type": pdata["type"],
                    "year": pdata["year"],
                    "read_time": pdata["read_time"],
                    "description": pdata["description"],
                    "image": pdata["cover"],
                    "content": pdata["content"],
                    "is_published": True,
                }
            )

        self.stdout.write(self.style.SUCCESS("Successfully synced real local photography and seeded ROHA studio data!"))
