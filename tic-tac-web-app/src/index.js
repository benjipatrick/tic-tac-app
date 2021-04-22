import React from 'react';
import ReactDOM from 'react-dom';

import './index.css'


function Square(props) {
      return (
        <div className={props.isButtonDisabled ? 'box noHover' : 'box'}>
            <button 
                className="button" 
                onClick={props.onClick}
                disabled={props.isButtonDisabled}
            >
                {props.value}
            </button>
        </div>
      );
  }
  
class Board extends React.Component {
  
    renderSquare(i) {
      const isButtonDisabled = this.props.winner !== -2 || this.props.squares[i] != null || !this.props.isPlayerTurn;
        return <Square 
        className='square'
        value={this.props.squares[i]} 
        onClick={() => this.props.onClick(i)}
        winner={this.props.winner}
        isButtonDisabled={isButtonDisabled}
        />;
    }

    render() {
        return (
            <div>
                <div className='game-board'>
                    {this.renderSquare(0)}{this.renderSquare(1)}{this.renderSquare(2)}
                    {this.renderSquare(3)}{this.renderSquare(4)}{this.renderSquare(5)}
                    {this.renderSquare(6)}{this.renderSquare(7)}{this.renderSquare(8)}
                </div>
            </div>
        );
    }
}


  
class Game extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        squares: Array(9).fill(null),
        isXTurn: true,
        winner: -2,
    };

    this.handleClick = this.handleClick.bind(this);
    this.handlePress = this.handlePress.bind(this);
  }

  componentDidMount() {

  }

  async GetGameStatus(squares, endOfPlayerTurn) {
    console.log("Making Game Status Request")
    try {
      const response = await fetch('https://tic-tac-app-me.herokuapp.com/game/status', {
        method:"POST",
          cache: "no-cache",
          headers:{
              "content_type":"application/json",
          },
          body:JSON.stringify(squares)
        })
      if (!response.ok) {
        throw Error(response.statusText)
      }
      const json = await response.json();

      const nextMove = json[1]
      var status = JSON.stringify(json[0]);
      console.log(status)
      console.log(nextMove)
      if (status === 'null') {
        status = -2
      }

      this.setState({
        winner:status
      })
      
      if (!endOfPlayerTurn && status == -2) {
        squares = this.state.squares.slice()
        if (nextMove == 'null') {
          squares[squares.indexOf(null)] = 'O'
        } else {
          squares[nextMove] = 'O'
        }
        
        this.setState({
          squares:squares,
          isXTurn: !this.state.isXTurn,
        })
        this.GetGameStatus(squares, true)
      } 
      
     
  
    } catch (error) {
      console.log(error)
    }
  }

  handleClick(i) {
    const squares = this.state.squares.slice();
    squares[i] = this.state.isXTurn ? 'X' : 'O';

    this.setState({
      squares: squares,
      isXTurn: !this.state.isXTurn,  
    })

    this.GetGameStatus(squares, false)
  }

  handlePress() {
    this.setState({
        squares: Array(9).fill(null),
        isXTurn: true,
        winner: -2,
    });
  }

  render() {

    var playerInfo;

    if (this.state.winner == 0) {
      playerInfo = 'Draw';
    } else if (this.state.winner != -2) {
      playerInfo = (this.state.winner==1 ? 'X' : 'O')   + ' Wins!!!';
    } else {
      playerInfo = 'Player Turn: ' +  (this.state.isXTurn ? 'X' : 'O');
    }


    return (
      <div className="game">
          <Board 
            squares={this.state.squares}
            onClick={(i) => this.handleClick(i)}
            winner={this.state.winner}
            isPlayerTurn={this.state.isXTurn}
          />
        <div className="game-info">
          <div className="current-player">{playerInfo}</div>
          <br></br>
          <button 
              className="restart-button"
              onClick={() => this.handlePress()}
              >Reset</button>
        </div>
      </div>
    );
  }
}
  
  // ========================================
  
  ReactDOM.render(
    <Game />,
    document.getElementById('root')
  );
