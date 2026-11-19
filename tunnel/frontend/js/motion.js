/**
 * KORYXA Motion Design Framework
 * Powered by GSAP & ScrollTrigger
 * -------------------------------------------------------------
 * Architecturé pour une performance 60fps, responsive mobile-first,
 * respectant la préférence d'accessibilité prefers-reduced-motion.
 */

document.addEventListener("DOMContentLoaded", () => {
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // 1. Initialisation GSAP & ScrollTrigger si disponible
  if (typeof gsap !== "undefined") {
    if (typeof ScrollTrigger !== "undefined") {
      gsap.registerPlugin(ScrollTrigger);
    }

    if (!prefersReducedMotion) {
      initHeroAnimations();
      initScrollTriggers();
      initBook3DTilt();
    }
  }

  // 2. Initialisation des composants interactifs (fonctionnent toujours, même sans motion)
  initInteractiveRagSimulator();
  initStickyConversionDock();
  initBentoInteractivity();
});

/**
 * Animation d'introduction du Hero au chargement de page
 */
function initHeroAnimations() {
  const tl = gsap.timeline({ defaults: { ease: "power3.out" } });

  tl.from(".hero-tagline", {
    opacity: 0,
    y: -16,
    duration: 0.6,
    delay: 0.1,
  })
  .from(".hero-title", {
    opacity: 0,
    y: 24,
    duration: 0.8,
  }, "-=0.3")
  .from(".hero-subtitle", {
    opacity: 0,
    y: 18,
    duration: 0.7,
  }, "-=0.5")
  .from(".hero-cta-box", {
    opacity: 0,
    y: 20,
    duration: 0.7,
    scale: 0.98,
  }, "-=0.4")
  .from(".hero-visual-card", {
    opacity: 0,
    x: 30,
    duration: 0.9,
    ease: "power2.out",
  }, "-=0.6")
  .from(".book-3d", {
    rotationY: -25,
    rotationX: 10,
    opacity: 0,
    duration: 1.2,
    ease: "back.out(1.2)",
  }, "-=0.6")
  .from(".app-float-card", {
    opacity: 0,
    y: 25,
    scale: 0.94,
    duration: 0.8,
  }, "-=0.7")
  .from(".included-strip .included-item", {
    opacity: 0,
    y: 10,
    stagger: 0.1,
    duration: 0.5,
  }, "-=0.4");
}

/**
 * Effet 3D tactile au mouvement de la souris sur le Hero
 */
function initBook3DTilt() {
  const stage = document.querySelector(".hero-visual-card");
  const book = document.querySelector(".book-3d");
  const appFloat = document.querySelector(".app-float-card");
  if (!stage || !book) return;

  // Désactiver sur mobile / tactile pour préserver le scroll fluide
  if (window.innerWidth < 992) return;

  stage.addEventListener("mousemove", (e) => {
    const rect = stage.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top - rect.height / 2;

    const rotX = (y / (rect.height / 2)) * -10;
    const rotY = (x / (rect.width / 2)) * 12;

    gsap.to(book, {
      rotationX: rotX,
      rotationY: rotY - 8,
      duration: 0.5,
      ease: "power1.out",
      transformPerspective: 900,
    });

    if (appFloat) {
      gsap.to(appFloat, {
        x: (x / 20),
        y: (y / 20),
        duration: 0.5,
        ease: "power1.out",
      });
    }
  });

  stage.addEventListener("mouseleave", () => {
    gsap.to(book, {
      rotationX: 4,
      rotationY: -8,
      duration: 0.8,
      ease: "power2.out",
    });
    if (appFloat) {
      gsap.to(appFloat, {
        x: 0,
        y: 0,
        duration: 0.8,
        ease: "power2.out",
      });
    }
  });
}

/**
 * Révélations progressives au défilement (ScrollTrigger)
 */
function initScrollTriggers() {
  if (typeof ScrollTrigger === "undefined") return;

  // Sections en fade-up fluide
  gsap.utils.toArray(".motion-reveal-section").forEach((sec) => {
    gsap.from(sec, {
      scrollTrigger: {
        trigger: sec,
        start: "top 85%",
        toggleActions: "play none none none",
      },
      opacity: 0,
      y: 30,
      duration: 0.8,
      ease: "power2.out",
    });
  });

  // Grilles d'éléments étagés (Bento & Steps)
  gsap.utils.toArray(".stagger-grid").forEach((grid) => {
    const cards = grid.children;
    gsap.from(cards, {
      scrollTrigger: {
        trigger: grid,
        start: "top 82%",
        toggleActions: "play none none none",
      },
      opacity: 0,
      y: 25,
      stagger: 0.12,
      duration: 0.7,
      ease: "power2.out",
    });
  });
}

/**
 * 3. Simulateur RAG Interactif en Direct ("Live Engine")
 * Permet au visiteur de tester lui-même le remplacement documentaire à chaud
 */
function initInteractiveRagSimulator() {
  const btnV1 = document.getElementById("simDocV1");
  const btnV2 = document.getElementById("simDocV2");
  const assistantBubble = document.getElementById("simAssistantResponse");
  const citationBadge = document.getElementById("simCitationBadge");
  const latencyBadge = document.getElementById("simLatencyBadge");
  const statusBar = document.getElementById("simStatusBar");
  const docBadge = document.getElementById("simDocActiveBadge");

  if (!btnV1 || !btnV2 || !assistantBubble) return;

  const dataset = {
    v1: {
      docName: "02_tarifs_et_financements_v1.pdf (650 €)",
      answer: "Le tarif total pour le parcours Analyse de Données est de <strong>650 euros</strong> (frais administratifs de 40 euros inclus), payable en trois tranches de 220 €, 220 € et 210 €.",
      citation: "02_tarifs_et_financements.pdf (page 1, section 2.1)",
      latency: "1.2s",
      tagColor: "#3B82F6",
    },
    v2: {
      docName: "02_tarifs_et_financements_v2.pdf (700 €)",
      answer: "Suite au remplacement du document tarifaire, le nouveau tarif total pour Analyse de Données est de <strong>700 euros</strong>, avec trois mensualités réajustées à 240 €, 230 € et 230 €.",
      citation: "02_tarifs_et_financements_v2.pdf (page 1, mise à jour)",
      latency: "1.1s",
      tagColor: "#EA580C",
    }
  };

  function updateSimulation(versionKey) {
    const data = dataset[versionKey];

    // Animation de transition
    btnV1.classList.toggle("active", versionKey === "v1");
    btnV2.classList.toggle("active", versionKey === "v2");

    if (statusBar) {
      statusBar.innerHTML = `<span style="color: #F59E0B;"><i data-lucide="loader-2" class="animate-spin" style="width: 14px; display: inline;"></i> Ingestion vectorielle Cohere Embed v4 en cours...</span>`;
      if (window.lucide) lucide.createIcons();
    }

    assistantBubble.style.opacity = "0.4";

    setTimeout(() => {
      assistantBubble.innerHTML = data.answer;
      assistantBubble.style.opacity = "1";

      if (citationBadge) {
        citationBadge.innerHTML = `<i data-lucide="paperclip" style="width: 12px; display: inline;"></i> ${data.citation}`;
      }

      if (latencyBadge) {
        latencyBadge.textContent = `Latence réelle : ${data.latency}`;
      }

      if (docBadge) {
        docBadge.textContent = data.docName;
        docBadge.style.borderColor = data.tagColor;
      }

      if (statusBar) {
        statusBar.innerHTML = `<span style="color: #10B981;"><i data-lucide="check-circle" style="width: 14px; display: inline;"></i> Document ingéré avec succès &middot; Index vectoriel synchronisé</span>`;
        if (window.lucide) lucide.createIcons();
      }
    }, 450);
  }

  btnV1.addEventListener("click", () => updateSimulation("v1"));
  btnV2.addEventListener("click", () => updateSimulation("v2"));
}

/**
 * 4. Sticky Conversion Dock
 * Apparaît au défilement en bas d'écran avec accès direct à l'achat et à l'espace
 */
function initStickyConversionDock() {
  const dock = document.getElementById("stickyConversionDock");
  if (!dock) return;

  let lastScroll = 0;
  window.addEventListener("scroll", () => {
    const currentScroll = window.scrollY;
    // Apparaît après avoir scrollé plus de 450px
    if (currentScroll > 450) {
      dock.classList.add("visible");
    } else {
      dock.classList.remove("visible");
    }
    lastScroll = currentScroll;
  }, { passive: true });
}

/**
 * 5. Bento Grid Interactivité
 */
function initBentoInteractivity() {
  const bentoCards = document.querySelectorAll(".bento-interactive-card");
  bentoCards.forEach((card) => {
    card.addEventListener("mouseenter", () => {
      card.style.transform = "translateY(-4px)";
    });
    card.addEventListener("mouseleave", () => {
      card.style.transform = "translateY(0)";
    });
  });
}
