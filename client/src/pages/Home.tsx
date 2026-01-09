import React from 'react';
import mindePulseLogo from '../assets/logo2.png';

export default function Home() {
    return (
        <div id="tab-start" style={{ display: 'block' }}>

            <section className="start-hero">

                <img src={mindePulseLogo} alt="MindPulse Hero Logo" className="start-logo" />

                <div className="start-text-wrapper">
                    <div className="start-text">
                        MindPulse ist ein interdisziplinäres Semesterprojekt zur explorativen Analyse psychologischer Fragebogendaten.<br />
                        Die Anwendung unterstützt die strukturierte Auswertung von Itemantworten entlang der HiTOP-Dimensionen.<br />
                        Ziel ist es, komplexe Antwortmuster übersichtlich darzustellen und vergleichbar zu machen.<br />
                        Neben der Visualisierung individueller Profile ermöglicht MindPulse die Generierung standardisierter Kurzscreenings.<br />
                        Diese können angepasst, exportiert und anschließend ausgewertet werden.<br />
                        Der Fokus liegt auf Transparenz, Nachvollziehbarkeit und methodischer Sauberkeit.<br />
                        MindPulse versteht sich nicht als diagnostisches Instrument.<br />
                        Vielmehr dient es der prototypischen Exploration psychologischer Daten.<br />
                        Die Anwendung wurde im Rahmen eines Hochschulprojekts entwickelt.<br />
                        Sie zeigt exemplarisch, wie technische und psychologische Perspektiven zusammengeführt werden können.

                        <br /><br />

                    </div>
                </div>
            </section>
        </div>
    );
}
