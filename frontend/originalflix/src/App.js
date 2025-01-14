import About from "./components/about";
import Changelog from "./components/changelog";
import Header from "./components/header";
import Ticker from "./components/ticker";

function App() {
return (
    <main>
        <Header />
        <section className="text-center mt-10">
            <h3 className="text-2xl mb-6">Supported Streaming Services</h3>
            <Ticker />
        </section>
        <section className="flex flex-row items-center justify-around mt-10">
            <About />
            <Changelog />
        </section>
    </main>
);
}

export default App;
