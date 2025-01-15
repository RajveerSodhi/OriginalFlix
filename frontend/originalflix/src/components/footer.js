import { FaArrowRight } from "react-icons/fa";

function Footer() {
    return (
        <footer className="text-center p-4 flex flex-row justify-center items-center mt-8">
            <a
                href="mailto:rajveersodhi03@gmail.com"
                target="_blank"
                rel="noreferrer"
                className="flex flex-col p-4 justify-center items-center aspect-square h-36 bg-pink rounded-3xl shadow-md hover:shadow-lg hover:scale-105 transition-all duration-300 ease-in-out"
            >
                <span className="text-[3rem]">👋</span>
                <span className="text-[#000000] text-center">Say Hello</span>
            </a>
            <a
                href="https://www.rajveersodhi.com"
                target="_blank"
                rel="noreferrer"
                className="flex flex-col p-4 mx-8 justify-center items-center aspect-square h-36 bg-portfolio-bg rounded-3xl shadow-md hover:shadow-lg hover:scale-105 transition-all duration-300 ease-in-out"
            >
                <img className="h-[3rem] my-3" src="/portfolio.svg" />
                <span className="text-[#ffffff] text-center">See More</span>
            </a>
            <a
                href="https://buymeacoffee.com/rajveersodhi"
                target="_blank"
                rel="noreferrer"
                className="flex flex-col p-4 mr-8 justify-center items-center aspect-square h-36 bg-coffee-bg rounded-3xl shadow-md hover:shadow-lg hover:scale-105 transition-all duration-300 ease-in-out"
            >
                <img className="h-[4rem] my-1" src="/bmac.png" />
                <img className="h-[2rem]" src="/bmac_text.png" />
            </a>
            <div className="flex flex-col justify-start items-start h-full w-full">
                <a
                    className="flex items-center hover:scale-90 transition-all duration-300 ease-in-out cursor-pointer"
                    href="/"
                >
                    <FaArrowRight className="scale-90 mr-1" />
                    Home
                </a>
                <a
                    className="flex items-center hover:scale-90 transition-all duration-300 ease-in-out cursor-pointer"
                    href="https://api.originalflix.dev"
                >
                    <FaArrowRight className="scale-90 mr-1" />
                    Documentation
                </a>
                <a
                    className="flex items-center hover:scale-90 transition-all duration-300 ease-in-out cursor-pointer"
                    href="https://api.originalflix.dev/redoc"
                >
                    <FaArrowRight className="scale-90 mr-1" />
                    Redoc
                </a>
                <div className="flex flex-col justify-start items-start h-full mt-2 text-sm text-dark">
                    <p>
                        Maintained by{" "}
                        <a
                            href="https://linkedin.com/in/rajveersodhi"
                            target="_blank"
                            rel="noreferrer"
                            className="hover:underline"
                        >
                            <strong>Rajveer Sodhi</strong>
                        </a>{" "}
                        via{" "}
                        <a
                            href="https://github.com/rajveersodhi"
                            className="hover:underline"
                            target="_blank"
                            rel="noreferrer"
                        >
                            <strong>GitHub</strong>
                        </a>
                        .
                    </p>
                    <p>All rights reserved.</p>
                </div>
            </div>
        </footer>
    );
}

export default Footer;
