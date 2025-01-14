function Ticker() {
    const logos = [
        "/logos/netflix.png",
        "/logos/appletv+.png",
        "/logos/hulu.svg",
        "/logos/hotstar.png",
        "/logos/primevideo.png",
        "/logos/zee5.svg",
        "/logos/paramount+.svg",
        "/logos/max.png",
        "/logos/peacock.svg",
        "/logos/star.svg",
        "/logos/disney+.png",
    ];

    return (
        <div className="ticker-container">
            <div className="ticker-slide">
                {logos.map((logo, index) => (
                    <img key={index} src={logo} alt={`Logo ${index}`} />
                ))}
                {logos.map((logo, index) => (
                    <img key={`duplicate-${index}`} src={logo} alt={`Logo Duplicate ${index}`} />
                ))}
            </div>
        </div>
    );
}

export default Ticker;