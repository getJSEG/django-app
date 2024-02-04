import React, { Component } from "react";

export default class HomePage extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="navigation"> 
                <h1> 4EVER LOGO </h1>

                <nav> 
                    <ul>
                        <li> Locales </li>
                        <li> Productos </li>
                        <li> Inventario </li>
                        <li> Ventas </li>
                    </ul>
                </nav>
            </div>

        );
    }
}
