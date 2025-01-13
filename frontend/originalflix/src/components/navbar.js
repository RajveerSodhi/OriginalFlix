import DocsButton from "./docsButton";

function Navbar() {
    return (
        <nav className="flex flex-row justify-between items-center p-4 mb-8">
            <a href="/"><img src="/logo+name.png" alt="OriginalFlix name and logo" className="h-14"/></a>
            <DocsButton />
        </nav>
    );
    }
    
    export default Navbar;