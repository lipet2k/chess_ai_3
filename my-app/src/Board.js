import React from 'react';
import Chessboard from "chessboardjsx";
import $, { data } from 'jquery';
import { Button } from 'reactstrap';

class Board extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            board: "start",
            value: 0,
        };

        this.makeHumanMove = this.makeHumanMove.bind(this);
        this.getNext = this.getNext.bind(this);
        this.reset = this.reset.bind(this);
        this.initialize = this.initialize.bind(this);
        this.getPrevious = this.getPrevious.bind(this);
    }


    componentDidMount() {
        this.setState({ board: "start",  value: 0});
        console.log("Board Mounted");
    }

    async makeHumanMove(properties) {

        const response = await fetch('/makeMove',
        {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: 'POST', // *GET, POST, PUT, DELETE, etc.
            body: JSON.stringify(properties) // body data type must match "Content-Type" header
          });
        const data = await response.json();
        this.setState({board: data.board, value: data.value});
    }

    async getNext() {
        const response = await fetch('/next');
        const data = await response.json();
        this.setState({board: data.board, value: data.value});
    }

    async initialize() {
        const response = await fetch('/');
        const data = await response.json();
        return data.board
    }

    async reset() {
        const response = await fetch('/reset');
        const data = await response.json();
        this.setState({board: data.board, value: data.value})
    }
    
    async getPrevious() {
        const response = await fetch('/previous');
        const data = await response.json();
        this.setState({board: data.board, value: data.value})
    }

    renderValue() {
        var newContainer = document.getElementById("value-container");
        newContainer.innerHTML = this.state.value;
        console.log("update value");
    }
    
    render() {

        return (
            <div className="board">
                <Chessboard
                position={this.state.board}
                onDrop={this.makeHumanMove}/>

                <h1>{this.state.value}</h1>
    
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