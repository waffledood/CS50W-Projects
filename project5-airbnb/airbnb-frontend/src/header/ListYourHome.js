import classes from "./ListYourHome.module.css";

const ListYourHome = (props) => {
  return (
    <div className={`${classes.div} default-font`}>
      <a href="/" className={`${classes.a} link`}>
        Airbnb your home
      </a>
    </div>
  );
};

export default ListYourHome;
