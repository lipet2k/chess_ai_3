import React from 'react';
import Chessboard from "chessboardjsx";
import $ from 'jquery';
import { Button } from 'reactstrap';

class Board extends React.Component {

    state = {
    board: "start",
    value: 0,
    };
        // console.log(this.state.svg);
        // this.getNext = this.getNext.bind(this);
        // this.reset = this.reset.bind(this);
        // this.initialize = this.initialize.bind(this);
        // this.getPrevious = this.getPrevious.bind(this);

    async getNext() {
        const response = await fetch('/next');
        const data = await response.json();
        this.setState({svg: data.svg, value: data.value});
    }

    async initialize() {
        const response = await fetch('/');
        const data = await response.json();
        return data.svg
        // this.setState({svg: data.svg, value: data.value})
    }

    async reset() {
        const response = await fetch('/reset');
        const data = await response.json();
        this.setState({svg: data.svg, value: data.value})
    }
    
    async getPrevious() {
        const response = await fetch('/previous');
        const data = await response.json();
        this.setState({svg: data.svg, value: this.state.value})
    }

    // renderSvg() {
    //     if (this.state.svg !== null) {
    //     var container = document.getElementById("svg-container");
    //     container.innerHTML = this.state.svg;
    //     console.log("rendering")
    //     }
    // }

    renderValue() {
        var newContainer = document.getElementById("value-container");
        newContainer.innerHTML = this.state.value;
        console.log("update value");
    }
    
    render() {
        return (
            <div className="board">
                <Chessboard className="board" position={this.state.board}/>
    
                <div className="ui">
                    <Button color='primary' onClick={this.getNext}>Next</Button>
                    <Button color='primary' onClick={this.getPrevious}>Previous</Button>
                    <Button color='danger' onClick={this.reset}>Reset</Button>
                </div>
            </div>
        );
    }

}

export default Board;