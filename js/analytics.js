(function () {
  var cfg = window.VUCA_SITE_CONFIG || {};
  if (cfg.googleSiteVerification) {
    var m = document.createElement("meta");
    m.name = "google-site-verification";
    m.content = cfg.googleSiteVerification;
    document.head.appendChild(m);
  }
  if (cfg.bingSiteVerification) {
    var b = document.createElement("meta");
    b.name = "msvalidate.01";
    b.content = cfg.bingSiteVerification;
    document.head.appendChild(b);
  }
  if (!cfg.gaMeasurementId) return;
  var s = document.createElement("script");
  s.async = true;
  s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(cfg.gaMeasurementId);
  document.head.appendChild(s);
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag("js", new Date());
  gtag("config", cfg.gaMeasurementId);
})();
