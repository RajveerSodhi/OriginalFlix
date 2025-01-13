import DocsButton from "./docsButton";

function Header() {
    return (
        <section className="flex flex-row w-screen">
            <div className="text-[4.5rem] w-full flex items-start flex-col text-left justify-center pl-8">
            <strong className="mb-8  leading-[5.5rem]">The <em>EXACT</em> database you need.</strong>
            <DocsButton />
            </div>
            <div className="h-[33rem] relative w-full">
            <img src="/bg.jpg" className="aspect-auto h-full" />
            <div className="absolute top-0 right-0 left-0 bottom-0 bg-gradient-to-r from-background to-background/0 w-full h-full"></div>
            </div>
        </section>
    );
}

export default Header;