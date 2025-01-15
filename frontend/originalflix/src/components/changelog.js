import changelogContent from "../changelog_content"

function Changelog() {
    return(
        <section id="Changelog" className="max-h-[54rem] bg-gradient-to-r from-pink to-orange w-full lg:ml-8 rounded-2xl p-2 shadow-md hover:scale-[1.01] hover:shadow-lg transition-all duration-300 ease-in-out">
            <div className="h-full w-full bg-dark/60 rounded-xl max-h-[53rem] overflow-y-scroll p-4">
                <h3 className="text-2xl text-light font-bold">Changelog</h3>

                {changelogContent.map((change, index) => (
                    <div key={index} className="my-4">
                        <p className="text-base text-light underline">{change.date}</p>
                        <ul className="ml-6 list-disc text-light">
                            {change.content.map((item, itemIndex) => (
                                <li key={itemIndex} className="mt-2">
                                    {item}
                                </li>
                            ))}
                        </ul>
                    </div>
                ))}

            </div>
        </section>
    );
}

export default Changelog